"""
Multi-objective optimization engine for CDST laboratory network optimization.
Implements NSGA-II algorithm using OR-Tools for solving the laboratory allocation problem.
"""

import asyncio
import math
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
from enum import Enum
import numpy as np
from ortools.linear_solver import pywraplp
from ortools.sat.python import cp_model
import structlog

from app.core.config import settings
from app.models.schemas import OptimizationWeights, OptimizationConstraints
from app.services.routing import RoutingService
from app.core.cache import cache_manager

logger = structlog.get_logger(__name__)


class OptimizationStatus(str, Enum):
    """Optimization status enumeration."""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass
class Laboratory:
    """Laboratory data structure for optimization."""
    id: str
    name: str
    latitude: float
    longitude: float
    max_tests_per_day: int
    max_tests_per_month: int
    staff_count: int
    equipment_count: int
    utilization_factor: float
    test_capabilities: Dict[str, Dict[str, Any]]
    operational_hours: Dict[str, Tuple[str, str]]


@dataclass
class ServiceArea:
    """Service area data structure for optimization."""
    id: str
    name: str
    latitude: float
    longitude: float
    population: int
    priority_level: int
    accessibility_index: float


@dataclass
class TestDemand:
    """Test demand data structure for optimization."""
    area_id: str
    test_type: str
    test_count: int
    priority_level: int
    urgency: str
    seasonal_factor: float


@dataclass
class Solution:
    """Optimization solution representation."""
    allocations: Dict[str, Dict[str, int]]  # {area_id: {lab_id: test_count}}
    objectives: Dict[str, float]
    constraints_satisfied: bool
    fitness_score: float
    metadata: Dict[str, Any]


class CDSTOptimizer:
    """Main optimization engine for CDST laboratory network optimization."""
    
    def __init__(self):
        self.routing_service = RoutingService()
        self.status = OptimizationStatus.PENDING
        self.progress = 0.0
        self.current_generation = 0
        self.best_solution: Optional[Solution] = None
        self.population: List[Solution] = []
        
    async def optimize_network(
        self,
        laboratories: List[Laboratory],
        service_areas: List[ServiceArea],
        test_demands: List[TestDemand],
        weights: OptimizationWeights,
        constraints: OptimizationConstraints,
        scenario_id: str
    ) -> Solution:
        """
        Main optimization method using NSGA-II multi-objective optimization.
        
        Args:
            laboratories: List of available laboratories
            service_areas: List of service areas requiring tests
            test_demands: List of test demand requirements
            weights: Objective function weights
            constraints: Optimization constraints
            scenario_id: Unique scenario identifier
            
        Returns:
            Optimized solution with allocations and metrics
        """
        logger.info("Starting network optimization", scenario_id=scenario_id)
        
        try:
            self.status = OptimizationStatus.RUNNING
            self.progress = 0.0
            
            # Step 1: Precompute distance and time matrices
            logger.info("Computing distance and time matrices")
            distance_matrix, time_matrix = await self._compute_matrices(
                laboratories, service_areas
            )
            self.progress = 0.1
            
            # Step 2: Initialize population
            logger.info("Initializing population")
            self.population = await self._initialize_population(
                laboratories, service_areas, test_demands, 
                distance_matrix, constraints
            )
            self.progress = 0.2
            
            # Step 3: Run NSGA-II optimization
            logger.info("Running NSGA-II optimization")
            best_solution = await self._run_nsga_ii(
                laboratories, service_areas, test_demands,
                distance_matrix, time_matrix, weights, constraints
            )
            
            self.status = OptimizationStatus.COMPLETED
            self.progress = 1.0
            self.best_solution = best_solution
            
            logger.info("Optimization completed successfully", 
                       scenario_id=scenario_id,
                       fitness_score=best_solution.fitness_score)
            
            return best_solution
            
        except Exception as e:
            self.status = OptimizationStatus.FAILED
            logger.error("Optimization failed", scenario_id=scenario_id, error=str(e))
            raise
    
    async def _compute_matrices(
        self, 
        laboratories: List[Laboratory], 
        service_areas: List[ServiceArea]
    ) -> Tuple[np.ndarray, np.ndarray]:
        """Compute distance and time matrices between all locations."""
        n_areas = len(service_areas)
        n_labs = len(laboratories)
        
        distance_matrix = np.zeros((n_areas, n_labs))
        time_matrix = np.zeros((n_areas, n_labs))
        
        # Use routing service to calculate distances and times
        for i, area in enumerate(service_areas):
            for j, lab in enumerate(laboratories):
                try:
                    # Try to get cached result first
                    cache_key = f"route_{area.id}_{lab.id}"
                    cached_result = await cache_manager.get(cache_key)
                    
                    if cached_result:
                        distance_matrix[i, j] = cached_result["distance"]
                        time_matrix[i, j] = cached_result["time"]
                    else:
                        # Calculate route
                        route_result = await self.routing_service.calculate_route(
                            (area.latitude, area.longitude),
                            (lab.latitude, lab.longitude)
                        )
                        
                        distance_matrix[i, j] = route_result.distance_km
                        time_matrix[i, j] = route_result.duration_minutes
                        
                        # Cache result
                        await cache_manager.set(
                            cache_key,
                            {
                                "distance": route_result.distance_km,
                                "time": route_result.duration_minutes
                            },
                            ttl=3600  # Cache for 1 hour
                        )
                        
                except Exception as e:
                    logger.warning(f"Failed to calculate route from {area.id} to {lab.id}", error=str(e))
                    # Use Haversine distance as fallback
                    distance_matrix[i, j] = self._haversine_distance(
                        area.latitude, area.longitude,
                        lab.latitude, lab.longitude
                    )
                    # Estimate time based on distance (assuming 50 km/h average speed)
                    time_matrix[i, j] = distance_matrix[i, j] / 50.0 * 60
        
        return distance_matrix, time_matrix
    
    async def _initialize_population(
        self,
        laboratories: List[Laboratory],
        service_areas: List[ServiceArea],
        test_demands: List[TestDemand],
        distance_matrix: np.ndarray,
        constraints: OptimizationConstraints,
        population_size: int = None
    ) -> List[Solution]:
        """Initialize population with diverse solutions."""
        if population_size is None:
            population_size = settings.OPTIMIZATION_POPULATION_SIZE
        
        population = []
        
        # Generate diverse initial solutions
        for i in range(population_size):
            if i < population_size // 3:
                # Random initialization
                solution = await self._random_initialization(
                    laboratories, service_areas, test_demands, constraints
                )
            elif i < 2 * population_size // 3:
                # Greedy initialization (distance-based)
                solution = await self._greedy_initialization(
                    laboratories, service_areas, test_demands, 
                    distance_matrix, constraints
                )
            else:
                # Hybrid initialization
                solution = await self._hybrid_initialization(
                    laboratories, service_areas, test_demands,
                    distance_matrix, constraints
                )
            
            population.append(solution)
        
        return population
    
    async def _random_initialization(
        self,
        laboratories: List[Laboratory],
        service_areas: List[ServiceArea],
        test_demands: List[TestDemand],
        constraints: OptimizationConstraints
    ) -> Solution:
        """Create random feasible solution."""
        allocations = {}
        
        # Group demands by service area
        area_demands = {}
        for demand in test_demands:
            if demand.area_id not in area_demands:
                area_demands[demand.area_id] = []
            area_demands[demand.area_id].append(demand)
        
        # Randomly allocate tests while respecting constraints
        for area_id, demands in area_demands.items():
            allocations[area_id] = {}
            
            for demand in demands:
                # Find laboratories that can handle this test type
                capable_labs = [
                    lab for lab in laboratories
                    if demand.test_type in lab.test_capabilities
                    and lab.test_capabilities[demand.test_type].get("available", False)
                ]
                
                if capable_labs:
                    # Randomly select laboratory
                    selected_lab = np.random.choice(capable_labs)
                    
                    if selected_lab.id not in allocations[area_id]:
                        allocations[area_id][selected_lab.id] = 0
                    
                    allocations[area_id][selected_lab.id] += demand.test_count
        
        return self._create_solution(allocations, laboratories, service_areas, test_demands)
    
    async def _greedy_initialization(
        self,
        laboratories: List[Laboratory],
        service_areas: List[ServiceArea],
        test_demands: List[TestDemand],
        distance_matrix: np.ndarray,
        constraints: OptimizationConstraints
    ) -> Solution:
        """Create greedy solution based on minimum distance."""
        allocations = {}
        
        # Create mapping from IDs to indices
        area_id_to_idx = {area.id: i for i, area in enumerate(service_areas)}
        lab_id_to_idx = {lab.id: i for i, lab in enumerate(laboratories)}
        
        # Group demands by service area
        area_demands = {}
        for demand in test_demands:
            if demand.area_id not in area_demands:
                area_demands[demand.area_id] = []
            area_demands[demand.area_id].append(demand)
        
        # Allocate to nearest capable laboratory
        for area_id, demands in area_demands.items():
            allocations[area_id] = {}
            area_idx = area_id_to_idx[area_id]
            
            for demand in demands:
                # Find capable laboratories
                capable_labs = [
                    (lab, lab_id_to_idx[lab.id]) for lab in laboratories
                    if demand.test_type in lab.test_capabilities
                    and lab.test_capabilities[demand.test_type].get("available", False)
                ]
                
                if capable_labs:
                    # Select nearest laboratory
                    distances = [(lab, distance_matrix[area_idx, lab_idx]) 
                               for lab, lab_idx in capable_labs]
                    nearest_lab, _ = min(distances, key=lambda x: x[1])
                    
                    if nearest_lab.id not in allocations[area_id]:
                        allocations[area_id][nearest_lab.id] = 0
                    
                    allocations[area_id][nearest_lab.id] += demand.test_count
        
        return self._create_solution(allocations, laboratories, service_areas, test_demands)
    
    async def _hybrid_initialization(
        self,
        laboratories: List[Laboratory],
        service_areas: List[ServiceArea],
        test_demands: List[TestDemand],
        distance_matrix: np.ndarray,
        constraints: OptimizationConstraints
    ) -> Solution:
        """Create hybrid solution balancing distance and capacity."""
        allocations = {}
        lab_utilization = {lab.id: 0 for lab in laboratories}
        
        # Create mapping from IDs to indices
        area_id_to_idx = {area.id: i for i, area in enumerate(service_areas)}
        lab_id_to_idx = {lab.id: i for i, lab in enumerate(laboratories)}
        
        # Group demands by service area
        area_demands = {}
        for demand in test_demands:
            if demand.area_id not in area_demands:
                area_demands[demand.area_id] = []
            area_demands[demand.area_id].append(demand)
        
        # Allocate considering both distance and utilization
        for area_id, demands in area_demands.items():
            allocations[area_id] = {}
            area_idx = area_id_to_idx[area_id]
            
            for demand in demands:
                # Find capable laboratories
                capable_labs = [
                    lab for lab in laboratories
                    if demand.test_type in lab.test_capabilities
                    and lab.test_capabilities[demand.test_type].get("available", False)
                ]
                
                if capable_labs:
                    # Calculate hybrid score (distance + utilization penalty)
                    scores = []
                    for lab in capable_labs:
                        lab_idx = lab_id_to_idx[lab.id]
                        distance = distance_matrix[area_idx, lab_idx]
                        utilization = lab_utilization[lab.id] / lab.max_tests_per_day
                        
                        # Hybrid score: weighted combination of distance and utilization
                        score = distance * 0.7 + utilization * 100 * 0.3
                        scores.append((lab, score))
                    
                    # Select laboratory with best hybrid score
                    best_lab, _ = min(scores, key=lambda x: x[1])
                    
                    if best_lab.id not in allocations[area_id]:
                        allocations[area_id][best_lab.id] = 0
                    
                    allocations[area_id][best_lab.id] += demand.test_count
                    lab_utilization[best_lab.id] += demand.test_count
        
        return self._create_solution(allocations, laboratories, service_areas, test_demands)
    
    async def _run_nsga_ii(
        self,
        laboratories: List[Laboratory],
        service_areas: List[ServiceArea],
        test_demands: List[TestDemand],
        distance_matrix: np.ndarray,
        time_matrix: np.ndarray,
        weights: OptimizationWeights,
        constraints: OptimizationConstraints
    ) -> Solution:
        """Run NSGA-II multi-objective optimization algorithm."""
        max_generations = settings.OPTIMIZATION_MAX_GENERATIONS
        
        for generation in range(max_generations):
            self.current_generation = generation
            self.progress = 0.2 + (generation / max_generations) * 0.7
            
            # Evaluate population
            await self._evaluate_population(
                self.population, laboratories, service_areas, test_demands,
                distance_matrix, time_matrix, weights
            )
            
            # Non-dominated sorting
            fronts = self._non_dominated_sort(self.population)
            
            # Calculate crowding distance
            for front in fronts:
                self._calculate_crowding_distance(front)
            
            # Selection for next generation
            new_population = []
            for front in fronts:
                if len(new_population) + len(front) <= len(self.population):
                    new_population.extend(front)
                else:
                    # Sort by crowding distance and take best
                    front.sort(key=lambda x: x.metadata.get("crowding_distance", 0), reverse=True)
                    remaining = len(self.population) - len(new_population)
                    new_population.extend(front[:remaining])
                    break
            
            # Generate offspring through crossover and mutation
            offspring = await self._generate_offspring(
                new_population, laboratories, service_areas, test_demands, constraints
            )
            
            # Combine parent and offspring populations
            self.population = new_population + offspring
            
            # Log progress
            if generation % 10 == 0:
                best_fitness = max(sol.fitness_score for sol in self.population)
                logger.info(f"Generation {generation}: Best fitness = {best_fitness:.4f}")
        
        # Return best solution from final population
        await self._evaluate_population(
            self.population, laboratories, service_areas, test_demands,
            distance_matrix, time_matrix, weights
        )
        
        return max(self.population, key=lambda x: x.fitness_score)
    
    def _create_solution(
        self,
        allocations: Dict[str, Dict[str, int]],
        laboratories: List[Laboratory],
        service_areas: List[ServiceArea],
        test_demands: List[TestDemand]
    ) -> Solution:
        """Create solution object from allocations."""
        return Solution(
            allocations=allocations,
            objectives={},
            constraints_satisfied=True,
            fitness_score=0.0,
            metadata={}
        )
    
    def _haversine_distance(self, lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """Calculate Haversine distance between two points."""
        R = settings.HAVERSINE_EARTH_RADIUS  # Earth radius in km
        
        lat1_rad = math.radians(lat1)
        lon1_rad = math.radians(lon1)
        lat2_rad = math.radians(lat2)
        lon2_rad = math.radians(lon2)
        
        dlat = lat2_rad - lat1_rad
        dlon = lon2_rad - lon1_rad
        
        a = (math.sin(dlat/2)**2 + 
             math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon/2)**2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
        
        return R * c
    
    async def _evaluate_population(
        self,
        population: List[Solution],
        laboratories: List[Laboratory],
        service_areas: List[ServiceArea],
        test_demands: List[TestDemand],
        distance_matrix: np.ndarray,
        time_matrix: np.ndarray,
        weights: OptimizationWeights
    ) -> None:
        """Evaluate all solutions in the population."""
        for solution in population:
            objectives = await self._calculate_objectives(
                solution, laboratories, service_areas, test_demands,
                distance_matrix, time_matrix
            )
            
            solution.objectives = objectives
            solution.fitness_score = self._calculate_weighted_fitness(objectives, weights)
    
    async def _calculate_objectives(
        self,
        solution: Solution,
        laboratories: List[Laboratory],
        service_areas: List[ServiceArea],
        test_demands: List[TestDemand],
        distance_matrix: np.ndarray,
        time_matrix: np.ndarray
    ) -> Dict[str, float]:
        """Calculate objective function values for a solution."""
        # Create mappings
        area_id_to_idx = {area.id: i for i, area in enumerate(service_areas)}
        lab_id_to_idx = {lab.id: i for i, lab in enumerate(laboratories)}
        
        # Initialize objectives
        total_distance = 0.0
        total_time = 0.0
        total_cost = 0.0
        total_tests = 0
        lab_utilization = {lab.id: 0 for lab in laboratories}
        
        # Calculate objectives from allocations
        for area_id, lab_allocations in solution.allocations.items():
            area_idx = area_id_to_idx[area_id]
            
            for lab_id, test_count in lab_allocations.items():
                lab_idx = lab_id_to_idx[lab_id]
                lab = laboratories[lab_idx]
                
                # Distance objective (minimize)
                distance = distance_matrix[area_idx, lab_idx]
                total_distance += distance * test_count
                
                # Time objective (minimize)
                time = time_matrix[area_idx, lab_idx]
                total_time += time * test_count
                
                # Cost objective (minimize) - simplified cost model
                base_cost = 25.0  # Base cost per test
                transport_cost = distance * 0.5  # Transport cost per km
                total_cost += (base_cost + transport_cost) * test_count
                
                # Update utilization
                lab_utilization[lab_id] += test_count
                total_tests += test_count
        
        # Calculate utilization objective (maximize)
        utilization_scores = []
        for lab in laboratories:
            if lab.max_tests_per_day > 0:
                utilization = lab_utilization[lab.id] / lab.max_tests_per_day
                utilization_scores.append(min(utilization, 1.0))
        
        avg_utilization = np.mean(utilization_scores) if utilization_scores else 0.0
        
        # Calculate accessibility objective (maximize)
        # Simplified: based on average distance
        avg_distance = total_distance / total_tests if total_tests > 0 else 0.0
        accessibility = 1.0 / (1.0 + avg_distance / 50.0)  # Normalize to 0-1
        
        return {
            "distance": total_distance,
            "time": total_time,
            "cost": total_cost,
            "utilization": avg_utilization,
            "accessibility": accessibility
        }
    
    def _calculate_weighted_fitness(
        self, 
        objectives: Dict[str, float], 
        weights: OptimizationWeights
    ) -> float:
        """Calculate weighted fitness score from objectives."""
        # Normalize objectives (assuming some reasonable ranges)
        normalized_objectives = {
            "distance": 1.0 - min(objectives["distance"] / 10000.0, 1.0),  # Lower is better
            "time": 1.0 - min(objectives["time"] / 5000.0, 1.0),  # Lower is better  
            "cost": 1.0 - min(objectives["cost"] / 100000.0, 1.0),  # Lower is better
            "utilization": objectives["utilization"],  # Higher is better
            "accessibility": objectives["accessibility"]  # Higher is better
        }
        
        # Calculate weighted sum
        fitness = (
            normalized_objectives["distance"] * weights.distance_weight +
            normalized_objectives["time"] * weights.time_weight +
            normalized_objectives["cost"] * weights.cost_weight +
            normalized_objectives["utilization"] * weights.utilization_weight +
            normalized_objectives["accessibility"] * weights.accessibility_weight
        )
        
        return fitness
    
    def _non_dominated_sort(self, population: List[Solution]) -> List[List[Solution]]:
        """Perform non-dominated sorting for NSGA-II."""
        fronts = [[]]
        
        for p in population:
            p.metadata["domination_count"] = 0
            p.metadata["dominated_solutions"] = []
            
            for q in population:
                if self._dominates(p, q):
                    p.metadata["dominated_solutions"].append(q)
                elif self._dominates(q, p):
                    p.metadata["domination_count"] += 1
            
            if p.metadata["domination_count"] == 0:
                p.metadata["rank"] = 0
                fronts[0].append(p)
        
        i = 0
        while len(fronts[i]) > 0:
            next_front = []
            for p in fronts[i]:
                for q in p.metadata["dominated_solutions"]:
                    q.metadata["domination_count"] -= 1
                    if q.metadata["domination_count"] == 0:
                        q.metadata["rank"] = i + 1
                        next_front.append(q)
            i += 1
            fronts.append(next_front)
        
        return fronts[:-1]  # Remove empty last front
    
    def _dominates(self, solution1: Solution, solution2: Solution) -> bool:
        """Check if solution1 dominates solution2."""
        # For maximization objectives, we want higher values
        # For minimization objectives, we want lower values
        
        obj1 = solution1.objectives
        obj2 = solution2.objectives
        
        # Convert to maximization problem
        values1 = [
            -obj1["distance"],  # Minimize distance
            -obj1["time"],      # Minimize time
            -obj1["cost"],      # Minimize cost
            obj1["utilization"], # Maximize utilization
            obj1["accessibility"] # Maximize accessibility
        ]
        
        values2 = [
            -obj2["distance"],
            -obj2["time"],
            -obj2["cost"],
            obj2["utilization"],
            obj2["accessibility"]
        ]
        
        # Check domination
        at_least_one_better = False
        for v1, v2 in zip(values1, values2):
            if v1 < v2:
                return False
            elif v1 > v2:
                at_least_one_better = True
        
        return at_least_one_better
    
    def _calculate_crowding_distance(self, front: List[Solution]) -> None:
        """Calculate crowding distance for solutions in a front."""
        if len(front) <= 2:
            for solution in front:
                solution.metadata["crowding_distance"] = float("inf")
            return
        
        # Initialize crowding distance
        for solution in front:
            solution.metadata["crowding_distance"] = 0.0
        
        # Calculate for each objective
        objectives = ["distance", "time", "cost", "utilization", "accessibility"]
        
        for obj in objectives:
            # Sort by objective
            front.sort(key=lambda x: x.objectives[obj])
            
            # Set boundary points to infinity
            front[0].metadata["crowding_distance"] = float("inf")
            front[-1].metadata["crowding_distance"] = float("inf")
            
            # Calculate range
            obj_range = front[-1].objectives[obj] - front[0].objectives[obj]
            if obj_range == 0:
                continue
            
            # Calculate crowding distance for intermediate points
            for i in range(1, len(front) - 1):
                distance = (front[i + 1].objectives[obj] - front[i - 1].objectives[obj]) / obj_range
                front[i].metadata["crowding_distance"] += distance
    
    async def _generate_offspring(
        self,
        population: List[Solution],
        laboratories: List[Laboratory],
        service_areas: List[ServiceArea],
        test_demands: List[TestDemand],
        constraints: OptimizationConstraints
    ) -> List[Solution]:
        """Generate offspring through crossover and mutation."""
        offspring = []
        
        for _ in range(len(population) // 2):
            # Tournament selection
            parent1 = self._tournament_selection(population)
            parent2 = self._tournament_selection(population)
            
            # Crossover
            child1, child2 = await self._crossover(parent1, parent2, laboratories, service_areas, test_demands)
            
            # Mutation
            child1 = await self._mutate(child1, laboratories, service_areas, test_demands, constraints)
            child2 = await self._mutate(child2, laboratories, service_areas, test_demands, constraints)
            
            offspring.extend([child1, child2])
        
        return offspring
    
    def _tournament_selection(self, population: List[Solution], tournament_size: int = 3) -> Solution:
        """Select parent using tournament selection."""
        tournament = np.random.choice(population, tournament_size, replace=False)
        return max(tournament, key=lambda x: x.fitness_score)
    
    async def _crossover(
        self,
        parent1: Solution,
        parent2: Solution,
        laboratories: List[Laboratory],
        service_areas: List[ServiceArea],
        test_demands: List[TestDemand]
    ) -> Tuple[Solution, Solution]:
        """Perform crossover between two parents."""
        # Simple uniform crossover
        child1_allocations = {}
        child2_allocations = {}
        
        all_areas = set(parent1.allocations.keys()) | set(parent2.allocations.keys())
        
        for area_id in all_areas:
            if np.random.random() < 0.5:
                child1_allocations[area_id] = parent1.allocations.get(area_id, {}).copy()
                child2_allocations[area_id] = parent2.allocations.get(area_id, {}).copy()
            else:
                child1_allocations[area_id] = parent2.allocations.get(area_id, {}).copy()
                child2_allocations[area_id] = parent1.allocations.get(area_id, {}).copy()
        
        child1 = self._create_solution(child1_allocations, laboratories, service_areas, test_demands)
        child2 = self._create_solution(child2_allocations, laboratories, service_areas, test_demands)
        
        return child1, child2
    
    async def _mutate(
        self,
        solution: Solution,
        laboratories: List[Laboratory],
        service_areas: List[ServiceArea],
        test_demands: List[TestDemand],
        constraints: OptimizationConstraints,
        mutation_rate: float = 0.1
    ) -> Solution:
        """Perform mutation on a solution."""
        if np.random.random() > mutation_rate:
            return solution
        
        # Create a copy of allocations
        new_allocations = {}
        for area_id, lab_allocations in solution.allocations.items():
            new_allocations[area_id] = lab_allocations.copy()
        
        # Random mutation: reassign some tests from one area
        if new_allocations:
            area_id = np.random.choice(list(new_allocations.keys()))
            area_allocations = new_allocations[area_id]
            
            if area_allocations:
                # Select random laboratory to mutate
                lab_id = np.random.choice(list(area_allocations.keys()))
                test_count = area_allocations[lab_id]
                
                # Find alternative laboratories
                area_demands = [d for d in test_demands if d.area_id == area_id]
                if area_demands:
                    # Find capable laboratories for the first demand type
                    test_type = area_demands[0].test_type
                    capable_labs = [
                        lab for lab in laboratories
                        if lab.id != lab_id
                        and test_type in lab.test_capabilities
                        and lab.test_capabilities[test_type].get("available", False)
                    ]
                    
                    if capable_labs:
                        # Move some tests to alternative laboratory
                        new_lab = np.random.choice(capable_labs)
                        move_count = min(test_count, np.random.randint(1, test_count + 1))
                        
                        area_allocations[lab_id] -= move_count
                        if area_allocations[lab_id] == 0:
                            del area_allocations[lab_id]
                        
                        if new_lab.id not in area_allocations:
                            area_allocations[new_lab.id] = 0
                        area_allocations[new_lab.id] += move_count
        
        return self._create_solution(new_allocations, laboratories, service_areas, test_demands)


# Global optimizer instance
cdst_optimizer = CDSTOptimizer()