# Optimization Algorithm Specifications - CDST Diagnostic Network Optimization Platform

## Overview

The CDST Diagnostic Network Optimization Platform employs multi-objective evolutionary algorithms to solve the complex problem of optimally allocating Culture and Drug Sensitivity Testing (CDST) services across healthcare networks. This document provides comprehensive specifications for the optimization algorithms, objective functions, constraints, and implementation details.

## Problem Definition

### Problem Type
- **Classification**: Multi-objective Combinatorial Optimization Problem
- **Domain**: Healthcare Resource Allocation
- **Complexity**: NP-Hard
- **Variables**: Discrete (laboratory-service area assignments)
- **Objectives**: 5 competing objectives to minimize/maximize

### Decision Variables

#### Primary Decision Variable
```
x[i,j,k] ∈ {0, 1, 2, ..., D[i,j,k]}
```
Where:
- `i` = Service area index (1 to N_areas)
- `j` = Laboratory index (1 to N_labs)
- `k` = Test type index (1 to N_tests)
- `x[i,j,k]` = Number of tests of type k from area i assigned to laboratory j
- `D[i,j,k]` = Maximum demand for test type k from area i

#### Auxiliary Variables
```
y[j] ∈ [0, 1]     # Utilization rate of laboratory j
z[i] ∈ [0, 1]     # Accessibility score for service area i
c[i,j,k] ≥ 0      # Cost of processing test k from area i at laboratory j
t[i,j] ≥ 0        # Travel time from area i to laboratory j
d[i,j] ≥ 0        # Distance from area i to laboratory j
```

## Objective Functions

### 1. Distance Minimization (f₁)
**Goal**: Minimize total transportation distance

```
f₁ = Σᵢ Σⱼ Σₖ (x[i,j,k] × d[i,j]) / Σᵢ Σⱼ Σₖ x[i,j,k]
```

**Components**:
- `d[i,j]`: Great circle distance between service area i and laboratory j
- Normalized by total number of tests to ensure scale independence

**Weight Range**: 0.15 - 0.35 (default: 0.25)

### 2. Time Optimization (f₂)
**Goal**: Minimize total transportation and processing time

```
f₂ = Σᵢ Σⱼ Σₖ (x[i,j,k] × (t[i,j] + p[j,k])) / Σᵢ Σⱼ Σₖ x[i,j,k]
```

**Components**:
- `t[i,j]`: Travel time from area i to laboratory j
- `p[j,k]`: Processing time for test type k at laboratory j
- Includes both transport and laboratory processing delays

**Weight Range**: 0.10 - 0.30 (default: 0.20)

### 3. Cost Reduction (f₃)
**Goal**: Minimize total operational costs

```
f₃ = Σᵢ Σⱼ Σₖ (x[i,j,k] × c[i,j,k])
```

**Cost Components**:
```
c[i,j,k] = transport_cost[i,j] + processing_cost[j,k] + overhead_cost[j]
```

Where:
- `transport_cost[i,j] = d[i,j] × cost_per_km`
- `processing_cost[j,k] = base_cost[j,k] × complexity_factor[k]`
- `overhead_cost[j] = fixed_cost[j] / monthly_capacity[j]`

**Weight Range**: 0.15 - 0.35 (default: 0.25)

### 4. Utilization Maximization (f₄)
**Goal**: Maximize laboratory capacity utilization while avoiding overload

```
f₄ = -Σⱼ utilization_score[j] / N_labs
```

**Utilization Score Calculation**:
```python
def calculate_utilization_score(utilization_rate):
    if utilization_rate < 0.3:
        return utilization_rate * 0.5  # Penalty for underutilization
    elif utilization_rate <= 0.9:
        return utilization_rate       # Optimal range
    else:
        return 0.9 - (utilization_rate - 0.9) * 2  # Penalty for overutilization
```

**Weight Range**: 0.10 - 0.30 (default: 0.20)

### 5. Accessibility Enhancement (f₅)
**Goal**: Maximize equitable access to testing services

```
f₅ = -Σᵢ accessibility_score[i] / N_areas
```

**Accessibility Score Calculation**:
```python
def calculate_accessibility_score(area_i):
    # Distance-based accessibility
    min_distance = min(d[i,j] for j in available_labs[i])
    distance_score = max(0, 1 - min_distance / max_acceptable_distance)
    
    # Population-weighted accessibility
    population_factor = log(population[i]) / log(max_population)
    
    # Service availability
    available_tests = sum(1 for k in test_types if any(x[i,j,k] > 0 for j in labs))
    availability_score = available_tests / total_test_types
    
    return (distance_score * 0.4 + population_factor * 0.3 + availability_score * 0.3)
```

**Weight Range**: 0.05 - 0.20 (default: 0.10)

## Constraints

### 1. Hard Constraints (Must be satisfied)

#### Demand Satisfaction Constraint
```
Σⱼ x[i,j,k] = D[i,k]  ∀i,k
```
All demand for each test type in each service area must be satisfied.

#### Laboratory Capacity Constraint
```
Σᵢ Σₖ (x[i,j,k] × time_per_test[j,k]) ≤ available_hours[j]  ∀j
```
Total processing time cannot exceed laboratory capacity.

#### Staff Availability Constraint
```
Σᵢ Σₖ (x[i,j,k] × staff_required[j,k]) ≤ total_staff[j] × working_hours  ∀j
```
Staff requirements cannot exceed available staff hours.

#### Test Capability Constraint
```
x[i,j,k] > 0 ⟹ capability[j,k] = True  ∀i,j,k
```
Tests can only be assigned to laboratories that offer that test type.

#### Non-negativity Constraint
```
x[i,j,k] ≥ 0  ∀i,j,k
```
All decision variables must be non-negative integers.

### 2. Soft Constraints (Preferential)

#### Maximum Distance Constraint
```
x[i,j,k] > 0 ⟹ d[i,j] ≤ max_distance  (penalty if violated)
```
**Default max_distance**: 50 km
**Penalty**: Exponential increase in cost function

#### Maximum Travel Time Constraint
```
x[i,j,k] > 0 ⟹ t[i,j] ≤ max_travel_time  (penalty if violated)
```
**Default max_travel_time**: 120 minutes
**Penalty**: Linear increase in time objective

#### Utilization Range Constraint
```
min_utilization ≤ utilization[j] ≤ max_utilization  (penalty if violated)
```
**Default range**: 30% - 90%
**Penalty**: Quadratic penalty for values outside range

#### Quality Threshold Constraint
```
x[i,j,k] > 0 ⟹ quality_score[j,k] ≥ min_quality  (penalty if violated)
```
**Default min_quality**: 0.7
**Penalty**: Weighted reduction in solution fitness

## Algorithm Selection and Configuration

### Primary Algorithm: NSGA-II (Non-dominated Sorting Genetic Algorithm II)

#### Algorithm Rationale
- **Multi-objective Optimization**: Naturally handles 5 competing objectives
- **Pareto Optimality**: Provides diverse set of non-dominated solutions
- **Scalability**: Proven performance on problems with 100+ variables
- **Robustness**: Handles mixed integer-continuous variables effectively

#### NSGA-II Configuration

```python
NSGA2_CONFIG = {
    "population_size": 200,           # Population size per generation
    "max_generations": 500,           # Maximum number of generations
    "crossover_rate": 0.9,           # Probability of crossover
    "mutation_rate": 0.05,           # Probability of mutation
    "tournament_size": 3,            # Tournament selection size
    "elite_size": 20,                # Number of elite solutions to preserve
    "convergence_threshold": 0.001,  # Convergence detection threshold
    "diversity_threshold": 0.1       # Minimum diversity requirement
}
```

#### Genetic Operators

##### 1. Selection: Tournament Selection
```python
def tournament_selection(population, tournament_size=3):
    """Select parents using tournament selection with crowding distance."""
    selected = []
    for _ in range(len(population)):
        tournament = random.sample(population, tournament_size)
        # Select based on dominance rank, then crowding distance
        winner = min(tournament, key=lambda x: (x.rank, -x.crowding_distance))
        selected.append(winner)
    return selected
```

##### 2. Crossover: Multi-point Integer Crossover
```python
def crossover(parent1, parent2, crossover_rate=0.9):
    """Multi-point crossover for integer decision variables."""
    if random.random() > crossover_rate:
        return parent1, parent2
    
    # Select multiple crossover points
    n_points = random.randint(1, 3)
    points = sorted(random.sample(range(len(parent1.genes)), n_points))
    
    child1, child2 = parent1.copy(), parent2.copy()
    
    for i in range(0, len(points), 2):
        start = points[i]
        end = points[i+1] if i+1 < len(points) else len(parent1.genes)
        child1.genes[start:end] = parent2.genes[start:end]
        child2.genes[start:end] = parent1.genes[start:end]
    
    return child1, child2
```

##### 3. Mutation: Adaptive Gaussian Mutation
```python
def mutation(individual, mutation_rate=0.05, generation=0, max_generations=500):
    """Adaptive mutation with decreasing intensity over generations."""
    # Adaptive mutation rate
    adaptive_rate = mutation_rate * (1 - generation / max_generations)
    
    for i in range(len(individual.genes)):
        if random.random() < adaptive_rate:
            # Gaussian mutation with constraint awareness
            current_value = individual.genes[i]
            max_value = get_max_demand(i)  # Context-dependent maximum
            
            # Gaussian perturbation
            sigma = max_value * 0.1 * (1 - generation / max_generations)
            perturbation = random.gauss(0, sigma)
            
            new_value = max(0, min(max_value, current_value + perturbation))
            individual.genes[i] = int(new_value)
    
    return individual
```

### Alternative Algorithms

#### 1. MOEA/D (Multi-Objective Evolutionary Algorithm based on Decomposition)
**Use Case**: When computational time is critical
**Configuration**:
```python
MOEAD_CONFIG = {
    "population_size": 150,
    "max_generations": 300,
    "neighborhood_size": 20,
    "replacement_probability": 0.9,
    "weight_vectors": "uniform"  # or "random"
}
```

#### 2. SPEA2 (Strength Pareto Evolutionary Algorithm 2)
**Use Case**: When solution diversity is paramount
**Configuration**:
```python
SPEA2_CONFIG = {
    "population_size": 100,
    "archive_size": 100,
    "max_generations": 400,
    "k_nearest": 1  # For density estimation
}
```

## Constraint Handling Strategies

### 1. Penalty Function Method
```python
def penalty_function(solution, constraints):
    """Calculate penalty for constraint violations."""
    penalty = 0
    
    for constraint in constraints:
        violation = constraint.calculate_violation(solution)
        if violation > 0:
            penalty += constraint.weight * (violation ** constraint.power)
    
    return penalty
```

### 2. Repair Mechanism
```python
def repair_solution(solution):
    """Repair infeasible solutions to satisfy hard constraints."""
    # Step 1: Ensure demand satisfaction
    for area in range(n_areas):
        for test_type in range(n_test_types):
            total_assigned = sum(solution.x[area][lab][test_type] for lab in range(n_labs))
            demand = get_demand(area, test_type)
            
            if total_assigned != demand:
                # Redistribute to satisfy demand
                redistribute_demand(solution, area, test_type, demand - total_assigned)
    
    # Step 2: Ensure capacity constraints
    for lab in range(n_labs):
        if is_over_capacity(solution, lab):
            reduce_load(solution, lab)
    
    return solution
```

### 3. Feasibility-Preserving Operators
```python
def feasible_crossover(parent1, parent2):
    """Crossover that maintains feasibility."""
    child1, child2 = standard_crossover(parent1, parent2)
    
    # Repair any constraint violations
    child1 = repair_solution(child1)
    child2 = repair_solution(child2)
    
    return child1, child2
```

## Performance Optimization Techniques

### 1. Parallel Evaluation
```python
def parallel_evaluate_population(population, n_processes=4):
    """Evaluate population fitness in parallel."""
    with multiprocessing.Pool(n_processes) as pool:
        fitness_values = pool.map(evaluate_individual, population)
    
    for individual, fitness in zip(population, fitness_values):
        individual.fitness = fitness
    
    return population
```

### 2. Incremental Evaluation
```python
class IncrementalEvaluator:
    """Cache and incrementally update fitness evaluations."""
    
    def __init__(self):
        self.cache = {}
        self.distance_matrix = None  # Pre-computed distances
        self.cost_matrix = None      # Pre-computed costs
    
    def evaluate(self, solution):
        """Evaluate solution with caching."""
        solution_hash = hash(solution)
        
        if solution_hash in self.cache:
            return self.cache[solution_hash]
        
        fitness = self._compute_fitness(solution)
        self.cache[solution_hash] = fitness
        
        return fitness
```

### 3. Problem Decomposition
```python
def hierarchical_optimization(network):
    """Decompose large networks into manageable subproblems."""
    # Level 1: Regional clustering
    regions = cluster_service_areas(network.service_areas)
    
    # Level 2: Optimize within regions
    regional_solutions = []
    for region in regions:
        sub_network = extract_subnetwork(network, region)
        solution = optimize_subnetwork(sub_network)
        regional_solutions.append(solution)
    
    # Level 3: Global coordination
    global_solution = coordinate_regions(regional_solutions)
    
    return global_solution
```

## Algorithm Termination Criteria

### 1. Maximum Generations
```python
def check_max_generations(generation, max_generations):
    return generation >= max_generations
```

### 2. Convergence Detection
```python
def check_convergence(population_history, window_size=50, threshold=0.001):
    """Detect convergence based on hypervolume indicator."""
    if len(population_history) < window_size:
        return False
    
    recent_hv = [calculate_hypervolume(pop) for pop in population_history[-window_size:]]
    hv_variance = np.var(recent_hv)
    
    return hv_variance < threshold
```

### 3. Time Limit
```python
def check_time_limit(start_time, max_time_minutes=15):
    """Enforce maximum optimization time."""
    elapsed_minutes = (time.time() - start_time) / 60
    return elapsed_minutes >= max_time_minutes
```

### 4. User Cancellation
```python
def check_user_cancellation():
    """Check for user-initiated cancellation."""
    return optimization_status.is_cancelled
```

## Solution Representation

### Encoding Scheme
```python
class Solution:
    """Solution representation for CDST optimization."""
    
    def __init__(self, n_areas, n_labs, n_test_types):
        # 3D array: [service_area][laboratory][test_type]
        self.x = np.zeros((n_areas, n_labs, n_test_types), dtype=int)
        self.fitness = None
        self.objectives = None
        self.rank = None
        self.crowding_distance = 0
        self.constraint_violations = []
    
    def encode(self):
        """Convert 3D array to 1D chromosome for genetic operations."""
        return self.x.flatten()
    
    def decode(self, chromosome):
        """Convert 1D chromosome back to 3D array."""
        self.x = chromosome.reshape((self.n_areas, self.n_labs, self.n_test_types))
    
    def copy(self):
        """Create deep copy of solution."""
        new_solution = Solution(self.n_areas, self.n_labs, self.n_test_types)
        new_solution.x = self.x.copy()
        return new_solution
```

### Initialization Strategies

#### 1. Random Initialization
```python
def random_initialization(n_areas, n_labs, n_test_types, demands):
    """Generate random feasible solution."""
    solution = Solution(n_areas, n_labs, n_test_types)
    
    for area in range(n_areas):
        for test_type in range(n_test_types):
            demand = demands[area][test_type]
            available_labs = get_capable_labs(test_type)
            
            # Randomly distribute demand among capable laboratories
            remaining_demand = demand
            for lab in available_labs[:-1]:
                allocation = random.randint(0, remaining_demand)
                solution.x[area][lab][test_type] = allocation
                remaining_demand -= allocation
            
            # Assign remaining demand to last laboratory
            solution.x[area][available_labs[-1]][test_type] = remaining_demand
    
    return solution
```

#### 2. Greedy Initialization
```python
def greedy_initialization(n_areas, n_labs, n_test_types, demands, distances):
    """Generate solution using greedy nearest-neighbor heuristic."""
    solution = Solution(n_areas, n_labs, n_test_types)
    
    for area in range(n_areas):
        for test_type in range(n_test_types):
            demand = demands[area][test_type]
            
            # Sort laboratories by distance
            available_labs = get_capable_labs(test_type)
            sorted_labs = sorted(available_labs, key=lambda lab: distances[area][lab])
            
            # Assign to nearest laboratory with capacity
            for lab in sorted_labs:
                capacity = get_remaining_capacity(lab, test_type)
                allocation = min(demand, capacity)
                solution.x[area][lab][test_type] = allocation
                demand -= allocation
                
                if demand == 0:
                    break
    
    return solution
```

#### 3. Hybrid Initialization
```python
def hybrid_initialization(population_size, problem_data):
    """Create diverse initial population using multiple strategies."""
    population = []
    
    # 30% random solutions
    for _ in range(int(0.3 * population_size)):
        solution = random_initialization(problem_data)
        population.append(solution)
    
    # 40% greedy solutions with perturbation
    for _ in range(int(0.4 * population_size)):
        solution = greedy_initialization(problem_data)
        solution = add_random_perturbation(solution, intensity=0.1)
        population.append(solution)
    
    # 30% heuristic-based solutions
    for _ in range(int(0.3 * population_size)):
        solution = capacity_balanced_initialization(problem_data)
        population.append(solution)
    
    return population
```

## Performance Metrics and Evaluation

### 1. Algorithm Performance Metrics

#### Hypervolume Indicator
```python
def calculate_hypervolume(pareto_front, reference_point):
    """Calculate hypervolume indicator for solution quality."""
    # Normalize objectives to [0,1]
    normalized_front = normalize_objectives(pareto_front)
    
    # Calculate hypervolume using Monte Carlo method
    n_samples = 100000
    dominated_samples = 0
    
    for _ in range(n_samples):
        sample_point = [random.random() for _ in range(len(reference_point))]
        
        if any(dominates(solution, sample_point) for solution in normalized_front):
            dominated_samples += 1
    
    return dominated_samples / n_samples
```

#### Convergence Rate
```python
def calculate_convergence_rate(generation_history):
    """Calculate rate of convergence to optimal front."""
    convergence_values = []
    
    for generation in generation_history:
        # Distance to known optimal front (if available)
        avg_distance = np.mean([
            min_distance_to_optimal(solution) for solution in generation
        ])
        convergence_values.append(avg_distance)
    
    return convergence_values
```

#### Diversity Metrics
```python
def calculate_diversity(pareto_front):
    """Calculate diversity of solutions in objective space."""
    if len(pareto_front) < 2:
        return 0
    
    distances = []
    for i, sol1 in enumerate(pareto_front):
        for j, sol2 in enumerate(pareto_front[i+1:], i+1):
            distance = euclidean_distance(sol1.objectives, sol2.objectives)
            distances.append(distance)
    
    return np.std(distances) / np.mean(distances)
```

### 2. Solution Quality Metrics

#### Optimization Improvement
```python
def calculate_improvement(baseline_solution, optimized_solution):
    """Calculate percentage improvement over baseline."""
    improvements = {}
    
    for i, objective_name in enumerate(['distance', 'time', 'cost', 'utilization', 'accessibility']):
        baseline_value = baseline_solution.objectives[i]
        optimized_value = optimized_solution.objectives[i]
        
        if objective_name in ['utilization', 'accessibility']:
            # Higher is better
            improvement = (optimized_value - baseline_value) / baseline_value * 100
        else:
            # Lower is better
            improvement = (baseline_value - optimized_value) / baseline_value * 100
        
        improvements[objective_name] = improvement
    
    return improvements
```

## Implementation Architecture

### 1. Core Optimization Engine
```python
class CDSTOptimizer:
    """Main optimization engine for CDST network optimization."""
    
    def __init__(self, config):
        self.config = config
        self.algorithm = self._initialize_algorithm()
        self.problem_data = None
        self.current_generation = 0
        self.best_solutions = []
        self.status = "initialized"
    
    def optimize(self, network_data, parameters):
        """Execute optimization process."""
        self.status = "running"
        self.problem_data = self._preprocess_data(network_data)
        
        try:
            # Initialize population
            population = self._initialize_population()
            
            # Evolution loop
            while not self._termination_criteria_met():
                population = self._evolve_generation(population)
                self._update_progress()
                
                if self._should_checkpoint():
                    self._save_checkpoint()
            
            # Extract final results
            pareto_front = self._extract_pareto_front(population)
            self.status = "completed"
            
            return self._format_results(pareto_front)
            
        except Exception as e:
            self.status = "failed"
            raise OptimizationError(f"Optimization failed: {str(e)}")
    
    def cancel(self):
        """Cancel running optimization."""
        self.status = "cancelled"
```

### 2. Progress Monitoring
```python
class OptimizationMonitor:
    """Monitor and report optimization progress."""
    
    def __init__(self, optimizer):
        self.optimizer = optimizer
        self.start_time = None
        self.progress_callbacks = []
    
    def start_monitoring(self):
        """Start progress monitoring."""
        self.start_time = time.time()
        
    def update_progress(self):
        """Update progress and notify callbacks."""
        progress_data = {
            "generation": self.optimizer.current_generation,
            "max_generations": self.optimizer.config["max_generations"],
            "elapsed_time": time.time() - self.start_time,
            "best_fitness": self._get_best_fitness(),
            "convergence": self._calculate_convergence(),
            "estimated_completion": self._estimate_completion()
        }
        
        for callback in self.progress_callbacks:
            callback(progress_data)
```

This comprehensive optimization algorithm specification provides the foundation for implementing a robust, scalable, and efficient multi-objective optimization system for the CDST Diagnostic Network Optimization Platform. The specifications cover all aspects from problem formulation to implementation details, ensuring that the development team has clear guidance for building a production-ready optimization engine.