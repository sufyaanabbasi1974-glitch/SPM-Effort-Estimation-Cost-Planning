"""
COCOMO (COnstructive COst MOdel) estimation logic
Implements Basic and Intermediate COCOMO models for effort and cost estimation
"""


class COCOMOCalculator:
    """
    COCOMO estimation calculator
    Implements Basic and Intermediate COCOMO models
    """
    
    # COCOMO coefficients for different project types
    BASIC_COEFFICIENTS = {
        'Organic': {'a': 2.4, 'b': 1.05},
        'Semi-Detached': {'a': 3.0, 'b': 1.12},
        'Embedded': {'a': 3.6, 'b': 1.20}
    }
    
    # Intermediate COCOMO effort multipliers (simplified subset)
    # In a real system, these would include all 15 effort multipliers
    EFFORT_MULTIPLIERS = {
        'Required Software Reliability': {
            'Very Low': 0.75, 'Low': 0.88, 'Nominal': 1.0, 'High': 1.15, 'Very High': 1.40
        },
        'Database Size': {
            'Low': 0.93, 'Nominal': 1.0, 'High': 1.08, 'Very High': 1.16
        },
        'Product Complexity': {
            'Simple': 0.70, 'Low': 0.85, 'Nominal': 1.0, 'High': 1.15, 'Very High': 1.30
        },
        'Team Experience': {
            'Junior': 1.20, 'Intermediate': 1.0, 'Senior': 0.85
        }
    }
    
    @staticmethod
    def calculate_basic_cocomo(kloc, project_type):
        """
        Calculate effort and duration using Basic COCOMO model
        
        Args:
            kloc (float): Project size in Kilo Lines of Code
            project_type (str): 'Organic', 'Semi-Detached', or 'Embedded'
            
        Returns:
            dict: {'effort': person-months, 'duration': months}
        """
        coefficients = COCOMOCalculator.BASIC_COEFFICIENTS.get(project_type, {'a': 3.0, 'b': 1.12})
        a = coefficients['a']
        b = coefficients['b']
        
        # Basic COCOMO formulas
        effort = a * (kloc ** b)
        duration = 2.5 + 0.2 * effort if effort > 0 else 0
        
        return {
            'effort': round(effort, 2),
            'duration': round(duration, 2)
        }
    
    @staticmethod
    def calculate_intermediate_cocomo(kloc, project_type, experience_level, multipliers_dict=None):
        """
        Calculate effort using Intermediate COCOMO with effort multipliers
        
        Args:
            kloc (float): Project size in KLOC
            project_type (str): 'Organic', 'Semi-Detached', or 'Embedded'
            experience_level (str): 'Junior', 'Intermediate', 'Senior'
            multipliers_dict (dict): Optional custom effort multiplier values
            
        Returns:
            dict: {'effort': person-months, 'duration': months, 'multiplier_impact': factor}
        """
        # Start with basic COCOMO
        basic = COCOMOCalculator.calculate_basic_cocomo(kloc, project_type)
        base_effort = basic['effort']
        
        # Apply effort multipliers
        total_multiplier = 1.0
        
        # Apply experience multiplier
        exp_multiplier = COCOMOCalculator.EFFORT_MULTIPLIERS['Team Experience'].get(
            experience_level, 1.0
        )
        total_multiplier *= exp_multiplier
        
        # Apply additional multipliers if provided
        if multipliers_dict:
            for key, value in multipliers_dict.items():
                if key in COCOMOCalculator.EFFORT_MULTIPLIERS:
                    multiplier_value = COCOMOCalculator.EFFORT_MULTIPLIERS[key].get(value, 1.0)
                    total_multiplier *= multiplier_value
        
        # Final effort with multipliers
        intermediate_effort = base_effort * total_multiplier
        duration = 2.5 + 0.2 * intermediate_effort if intermediate_effort > 0 else 0
        
        return {
            'effort': round(intermediate_effort, 2),
            'duration': round(duration, 2),
            'multiplier_impact': round(total_multiplier, 2),
            'base_effort': round(base_effort, 2)
        }
    
    @staticmethod
    def calculate_costs(effort, cost_per_person_month):
        """
        Calculate total project cost from effort
        
        Args:
            effort (float): Effort in person-months
            cost_per_person_month (float): Cost per person-month in currency
            
        Returns:
            dict: {'total_cost': cost, 'cost_per_phase': phase breakdown}
        """
        total_cost = effort * cost_per_person_month
        
        # Standard phase distribution: 40% design, 30% code, 20% test, 10% integration
        phases = {
            'Design': effort * 0.40 * cost_per_person_month,
            'Code': effort * 0.30 * cost_per_person_month,
            'Test': effort * 0.20 * cost_per_person_month,
            'Integration': effort * 0.10 * cost_per_person_month
        }
        
        return {
            'total_cost': round(total_cost, 2),
            'cost_per_phase': {k: round(v, 2) for k, v in phases.items()}
        }
    
    @staticmethod
    def apply_risk_adjustment(effort, cost, adjustment_factor):
        """
        Apply risk-based adjustment to effort and cost
        
        Args:
            effort (float): Current effort estimate
            cost (float): Current cost estimate
            adjustment_factor (float): Risk multiplier (0.8 to 1.5 typical range)
            
        Returns:
            dict: {'adjusted_effort': value, 'adjusted_cost': value, 'adjustment_factor': factor}
        """
        adjusted_effort = effort * adjustment_factor
        adjusted_cost = cost * adjustment_factor
        
        return {
            'adjusted_effort': round(adjusted_effort, 2),
            'adjusted_cost': round(adjusted_cost, 2),
            'adjustment_factor': round(adjustment_factor, 2)
        }
