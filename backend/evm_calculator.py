"""
EVM (Earned Value Management) calculator
Implements metrics and project status tracking
"""


class EVMCalculator:
    """
    Earned Value Management calculator
    Calculates variance metrics and project status indicators
    """
    
    @staticmethod
    def calculate_evm_metrics(planned_value, earned_value, actual_cost):
        """
        Calculate all EVM metrics
        
        Args:
            planned_value (float): PV - Budgeted cost of work scheduled
            earned_value (float): EV - Budgeted cost of work performed
            actual_cost (float): AC - Real cost incurred
            
        Returns:
            dict: Dictionary containing all EVM metrics
        """
        
        # Cost Variance = EV - AC (positive is good)
        cost_variance = earned_value - actual_cost
        
        # Schedule Variance = EV - PV (positive is good)
        schedule_variance = earned_value - planned_value
        
        # Cost Performance Index = EV / AC (>1 is good)
        cost_performance_index = earned_value / actual_cost if actual_cost > 0 else 0
        
        # Schedule Performance Index = EV / PV (>1 is good)
        schedule_performance_index = earned_value / planned_value if planned_value > 0 else 0
        
        return {
            'cost_variance': round(cost_variance, 2),
            'schedule_variance': round(schedule_variance, 2),
            'cost_performance_index': round(cost_performance_index, 2),
            'schedule_performance_index': round(schedule_performance_index, 2)
        }
    
    @staticmethod
    def determine_project_status(cost_variance, schedule_variance, cpi, spi):
        """
        Determine project health status: Green, Yellow, or Red
        
        Args:
            cost_variance (float): CV value
            schedule_variance (float): SV value
            cpi (float): Cost Performance Index
            spi (float): Schedule Performance Index
            
        Returns:
            dict: {'status': status_color, 'reason': explanation}
        """
        
        # Red: Critical issues
        if cpi < 0.90 or spi < 0.90 or cost_variance < -500 or schedule_variance < -500:
            return {
                'status': 'Red',
                'reason': 'Project is significantly over budget or behind schedule'
            }
        
        # Yellow: Warning signs
        elif cpi < 0.95 or spi < 0.95 or cost_variance < 0 or schedule_variance < 0:
            return {
                'status': 'Yellow',
                'reason': 'Project is slightly over budget or falling behind schedule'
            }
        
        # Green: On track
        else:
            return {
                'status': 'Green',
                'reason': 'Project is on track for budget and schedule'
            }
    
    @staticmethod
    def estimate_at_completion(budget_at_completion, cpi):
        """
        Estimate total project cost at completion (EAC)
        Formula: EAC = BAC / CPI
        
        Args:
            budget_at_completion (float): Total budgeted cost
            cpi (float): Cost Performance Index
            
        Returns:
            float: Estimated cost at completion
        """
        if cpi > 0:
            return round(budget_at_completion / cpi, 2)
        return budget_at_completion
    
    @staticmethod
    def estimate_to_complete(budget_at_completion, earned_value):
        """
        Estimate remaining work cost
        Formula: ETC = BAC - EV
        
        Args:
            budget_at_completion (float): Total budgeted cost
            earned_value (float): Current earned value
            
        Returns:
            float: Estimated cost to complete
        """
        return round(budget_at_completion - earned_value, 2)
