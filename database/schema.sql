-- CDST Diagnostic Network Optimization Platform
-- Database Schema Definition
-- PostgreSQL 15+ with PostGIS 3.3+

-- Enable PostGIS extension for geospatial data
CREATE EXTENSION IF NOT EXISTS postgis;
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- User Management Tables
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    username VARCHAR(255) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(50) NOT NULL CHECK (role IN ('administrator', 'analyst', 'viewer')),
    first_name VARCHAR(255),
    last_name VARCHAR(255),
    organization VARCHAR(255),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP WITH TIME ZONE
);

-- User Sessions for JWT token management
CREATE TABLE user_sessions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    token_hash VARCHAR(255) NOT NULL,
    expires_at TIMESTAMP WITH TIME ZONE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    is_revoked BOOLEAN DEFAULT FALSE
);

-- Laboratory Network Tables
CREATE TABLE laboratory_networks (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(255) NOT NULL,
    description TEXT,
    created_by UUID REFERENCES users(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE
);

-- Laboratory Information
CREATE TABLE laboratories (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    network_id UUID REFERENCES laboratory_networks(id) ON DELETE CASCADE,
    laboratory_id VARCHAR(255) NOT NULL, -- User-defined identifier
    name VARCHAR(255) NOT NULL,
    location GEOGRAPHY(POINT, 4326) NOT NULL, -- PostGIS geography type
    latitude DECIMAL(10, 8) NOT NULL,
    longitude DECIMAL(11, 8) NOT NULL,
    address TEXT,
    phone VARCHAR(50),
    email VARCHAR(255),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(network_id, laboratory_id)
);

-- Laboratory Operational Hours
CREATE TABLE laboratory_hours (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    laboratory_id UUID REFERENCES laboratories(id) ON DELETE CASCADE,
    day_of_week INTEGER NOT NULL CHECK (day_of_week BETWEEN 0 AND 6), -- 0=Sunday, 6=Saturday
    open_time TIME,
    close_time TIME,
    is_closed BOOLEAN DEFAULT FALSE
);

-- Laboratory Capacities and Resources
CREATE TABLE laboratory_capacities (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    laboratory_id UUID REFERENCES laboratories(id) ON DELETE CASCADE,
    max_tests_per_day INTEGER NOT NULL CHECK (max_tests_per_day > 0),
    max_tests_per_month INTEGER NOT NULL CHECK (max_tests_per_month > 0),
    staff_count INTEGER NOT NULL CHECK (staff_count > 0),
    equipment_count INTEGER DEFAULT 1,
    utilization_factor DECIMAL(3, 2) DEFAULT 0.80 CHECK (utilization_factor BETWEEN 0 AND 1),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Test Types and Capabilities
CREATE TABLE test_types (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(255) UNIQUE NOT NULL,
    description TEXT,
    category VARCHAR(100), -- e.g., 'culture', 'sensitivity', 'specialized'
    standard_duration_minutes INTEGER NOT NULL CHECK (standard_duration_minutes > 0),
    complexity_level INTEGER DEFAULT 1 CHECK (complexity_level BETWEEN 1 AND 5),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Laboratory Test Capabilities
CREATE TABLE laboratory_test_capabilities (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    laboratory_id UUID REFERENCES laboratories(id) ON DELETE CASCADE,
    test_type_id UUID REFERENCES test_types(id) ON DELETE CASCADE,
    is_available BOOLEAN DEFAULT TRUE,
    time_per_test_minutes INTEGER NOT NULL CHECK (time_per_test_minutes > 0),
    staff_required INTEGER DEFAULT 1 CHECK (staff_required > 0),
    equipment_utilization DECIMAL(3, 2) DEFAULT 0.50 CHECK (equipment_utilization BETWEEN 0 AND 1),
    cost_per_test DECIMAL(10, 2) DEFAULT 0.00,
    quality_score DECIMAL(3, 2) DEFAULT 1.00 CHECK (quality_score BETWEEN 0 AND 1),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(laboratory_id, test_type_id)
);

-- Service Areas and Demand Points
CREATE TABLE service_areas (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    network_id UUID REFERENCES laboratory_networks(id) ON DELETE CASCADE,
    area_id VARCHAR(255) NOT NULL, -- User-defined identifier
    name VARCHAR(255) NOT NULL,
    location GEOGRAPHY(POINT, 4326) NOT NULL,
    latitude DECIMAL(10, 8) NOT NULL,
    longitude DECIMAL(11, 8) NOT NULL,
    population INTEGER DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(network_id, area_id)
);

-- Historical Test Demand Data
CREATE TABLE test_demand (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    service_area_id UUID REFERENCES service_areas(id) ON DELETE CASCADE,
    test_type_id UUID REFERENCES test_types(id) ON DELETE CASCADE,
    demand_date DATE NOT NULL,
    test_count INTEGER NOT NULL CHECK (test_count >= 0),
    priority_level INTEGER DEFAULT 1 CHECK (priority_level BETWEEN 1 AND 5),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(service_area_id, test_type_id, demand_date)
);

-- Optimization Scenarios and Results
CREATE TABLE optimization_scenarios (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    network_id UUID REFERENCES laboratory_networks(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    created_by UUID REFERENCES users(id),
    parameters JSONB NOT NULL, -- Optimization parameters and weights
    status VARCHAR(50) DEFAULT 'pending' CHECK (status IN ('pending', 'running', 'completed', 'failed', 'cancelled')),
    started_at TIMESTAMP WITH TIME ZONE,
    completed_at TIMESTAMP WITH TIME ZONE,
    execution_time_seconds INTEGER,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Optimization Results
CREATE TABLE optimization_results (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    scenario_id UUID REFERENCES optimization_scenarios(id) ON DELETE CASCADE,
    service_area_id UUID REFERENCES service_areas(id) ON DELETE CASCADE,
    laboratory_id UUID REFERENCES laboratories(id) ON DELETE CASCADE,
    test_type_id UUID REFERENCES test_types(id) ON DELETE CASCADE,
    allocated_tests INTEGER NOT NULL CHECK (allocated_tests >= 0),
    distance_km DECIMAL(10, 3),
    travel_time_minutes INTEGER,
    transport_cost DECIMAL(10, 2),
    processing_cost DECIMAL(10, 2),
    total_cost DECIMAL(10, 2),
    utilization_score DECIMAL(3, 2),
    accessibility_score DECIMAL(3, 2),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Route Caching for Performance
CREATE TABLE route_cache (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    origin_lat DECIMAL(10, 8) NOT NULL,
    origin_lng DECIMAL(11, 8) NOT NULL,
    destination_lat DECIMAL(10, 8) NOT NULL,
    destination_lng DECIMAL(11, 8) NOT NULL,
    distance_km DECIMAL(10, 3),
    duration_minutes INTEGER,
    route_geometry TEXT, -- GeoJSON or encoded polyline
    provider VARCHAR(50) DEFAULT 'osrm', -- 'osrm', 'haversine'
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP WITH TIME ZONE DEFAULT (CURRENT_TIMESTAMP + INTERVAL '24 hours')
);

-- Audit Log for Compliance
CREATE TABLE audit_log (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id),
    action VARCHAR(255) NOT NULL,
    resource_type VARCHAR(100) NOT NULL,
    resource_id UUID,
    old_values JSONB,
    new_values JSONB,
    ip_address INET,
    user_agent TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- System Configuration
CREATE TABLE system_config (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    key VARCHAR(255) UNIQUE NOT NULL,
    value JSONB NOT NULL,
    description TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for Performance
CREATE INDEX idx_laboratories_location ON laboratories USING GIST(location);
CREATE INDEX idx_service_areas_location ON service_areas USING GIST(location);
CREATE INDEX idx_laboratories_network ON laboratories(network_id);
CREATE INDEX idx_test_demand_date ON test_demand(demand_date);
CREATE INDEX idx_optimization_results_scenario ON optimization_results(scenario_id);
CREATE INDEX idx_route_cache_coords ON route_cache(origin_lat, origin_lng, destination_lat, destination_lng);
CREATE INDEX idx_route_cache_expires ON route_cache(expires_at);
CREATE INDEX idx_audit_log_user_time ON audit_log(user_id, created_at);
CREATE INDEX idx_user_sessions_token ON user_sessions(token_hash);
CREATE INDEX idx_user_sessions_expires ON user_sessions(expires_at);

-- Functions for common operations
CREATE OR REPLACE FUNCTION calculate_haversine_distance(
    lat1 DECIMAL, lng1 DECIMAL, lat2 DECIMAL, lng2 DECIMAL
) RETURNS DECIMAL AS $$
DECLARE
    r DECIMAL := 6371; -- Earth's radius in kilometers
    dlat DECIMAL;
    dlng DECIMAL;
    a DECIMAL;
    c DECIMAL;
BEGIN
    dlat := RADIANS(lat2 - lat1);
    dlng := RADIANS(lng2 - lng1);
    a := SIN(dlat/2) * SIN(dlat/2) + COS(RADIANS(lat1)) * COS(RADIANS(lat2)) * SIN(dlng/2) * SIN(dlng/2);
    c := 2 * ATAN2(SQRT(a), SQRT(1-a));
    RETURN r * c;
END;
$$ LANGUAGE plpgsql IMMUTABLE;

-- Function to clean expired route cache
CREATE OR REPLACE FUNCTION clean_expired_routes() RETURNS INTEGER AS $$
DECLARE
    deleted_count INTEGER;
BEGIN
    DELETE FROM route_cache WHERE expires_at < CURRENT_TIMESTAMP;
    GET DIAGNOSTICS deleted_count = ROW_COUNT;
    RETURN deleted_count;
END;
$$ LANGUAGE plpgsql;

-- Trigger function for updating timestamps
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Apply update triggers to relevant tables
CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_laboratories_updated_at BEFORE UPDATE ON laboratories
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_laboratory_capacities_updated_at BEFORE UPDATE ON laboratory_capacities
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_laboratory_test_capabilities_updated_at BEFORE UPDATE ON laboratory_test_capabilities
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_optimization_scenarios_updated_at BEFORE UPDATE ON optimization_scenarios
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Insert default test types
INSERT INTO test_types (name, description, category, standard_duration_minutes, complexity_level) VALUES
('Culture Test - Basic', 'Basic bacterial culture identification', 'culture', 180, 2),
('Culture Test - Advanced', 'Advanced bacterial culture with extended identification', 'culture', 360, 4),
('Drug Sensitivity - Standard Panel', 'Standard antibiotic sensitivity testing', 'sensitivity', 240, 3),
('Drug Sensitivity - Extended Panel', 'Extended antibiotic sensitivity testing', 'sensitivity', 480, 4),
('Mycobacterium Culture', 'Specialized culture for tuberculosis', 'specialized', 720, 5),
('Fungal Culture', 'Fungal identification and sensitivity', 'specialized', 600, 4),
('Rapid Diagnostic Test', 'Point-of-care rapid testing', 'rapid', 30, 1);

-- Insert default system configuration
INSERT INTO system_config (key, value, description) VALUES
('optimization_weights', '{"distance": 0.25, "time": 0.20, "cost": 0.25, "utilization": 0.20, "accessibility": 0.10}', 'Default weights for multi-objective optimization'),
('routing_api_config', '{"provider": "osrm", "base_url": "https://router.project-osrm.org", "timeout": 30, "fallback_to_haversine": true}', 'Routing API configuration'),
('cache_settings', '{"route_cache_ttl_hours": 24, "cleanup_interval_hours": 6}', 'Caching configuration'),
('performance_limits', '{"max_laboratories": 100, "max_service_areas": 1000, "optimization_timeout_minutes": 15}', 'System performance limits');

-- Create materialized view for quick laboratory statistics
CREATE MATERIALIZED VIEW laboratory_statistics AS
SELECT 
    l.id,
    l.name,
    l.network_id,
    lc.max_tests_per_day,
    lc.max_tests_per_month,
    lc.staff_count,
    COUNT(ltc.test_type_id) as available_test_types,
    AVG(ltc.quality_score) as avg_quality_score,
    SUM(ltc.cost_per_test * ltc.equipment_utilization) as weighted_cost_score
FROM laboratories l
LEFT JOIN laboratory_capacities lc ON l.id = lc.laboratory_id
LEFT JOIN laboratory_test_capabilities ltc ON l.id = ltc.laboratory_id AND ltc.is_available = true
GROUP BY l.id, l.name, l.network_id, lc.max_tests_per_day, lc.max_tests_per_month, lc.staff_count;

-- Index for the materialized view
CREATE INDEX idx_laboratory_statistics_network ON laboratory_statistics(network_id);

-- Refresh function for the materialized view
CREATE OR REPLACE FUNCTION refresh_laboratory_statistics() RETURNS VOID AS $$
BEGIN
    REFRESH MATERIALIZED VIEW laboratory_statistics;
END;
$$ LANGUAGE plpgsql;