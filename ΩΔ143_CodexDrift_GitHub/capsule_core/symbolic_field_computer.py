"""
Symbolic Field Computer for ΩΔ143 Codex Drift 5D Capsule

Handles symbolic field computation, pattern recognition,
and mathematical symbol processing in 5D space.
"""

import sympy as sp
import numpy as np
from typing import Dict, List, Any, Optional, Union, Callable
from dataclasses import dataclass
from enum import Enum
import json

from .scrollmath_engine import ScrollVector, CodexDriftField


class SymbolicDomain(Enum):
    """Domains for symbolic field computation."""
    MATHEMATICAL = "mathematical"
    LOGICAL = "logical"
    GEOMETRIC = "geometric"
    TEMPORAL = "temporal"
    QUANTUM = "quantum"


@dataclass
class SymbolicExpression:
    """Represents a symbolic expression in the codex drift system."""
    expression: sp.Expr
    domain: SymbolicDomain
    variables: List[str]
    complexity: float
    field_binding: Optional[str] = None  # Field ID this expression is bound to
    
    def evaluate_at_vector(self, vector: ScrollVector) -> complex:
        """Evaluate the symbolic expression at a specific 5D vector."""
        try:
            # Map 5D vector components to symbolic variables
            substitutions = {}
            if len(self.variables) >= 1:
                substitutions[self.variables[0]] = vector.x
            if len(self.variables) >= 2:
                substitutions[self.variables[1]] = vector.y
            if len(self.variables) >= 3:
                substitutions[self.variables[2]] = vector.z
            if len(self.variables) >= 4:
                substitutions[self.variables[3]] = vector.temporal
            if len(self.variables) >= 5:
                substitutions[self.variables[4]] = vector.symbolic
            
            result = self.expression.subs(substitutions)
            return complex(result.evalf())
        except Exception:
            return complex(0, 0)


@dataclass
class SymbolicField:
    """Represents a field of symbolic expressions."""
    expressions: List[SymbolicExpression]
    field_name: str
    dimension: int = 5
    coherence: float = 1.0
    

class SymbolicFieldComputer:
    """
    Computes symbolic fields and mathematical transformations
    for the ΩΔ143 Codex Drift system.
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initialize the symbolic field computer."""
        self.config = config or {}
        self.symbolic_fields: Dict[str, SymbolicField] = {}
        self.expression_cache: Dict[str, SymbolicExpression] = {}
        
        # Define symbolic variables for 5D computation
        self.vars_5d = sp.symbols('x y z t s', real=True)  # x,y,z,temporal,symbolic
        self.vars_dict = {
            'x': self.vars_5d[0],
            'y': self.vars_5d[1], 
            'z': self.vars_5d[2],
            't': self.vars_5d[3],
            's': self.vars_5d[4]
        }
        
        # Initialize fundamental symbolic expressions
        self._initialize_fundamental_expressions()
    
    def _initialize_fundamental_expressions(self):
        """Initialize fundamental symbolic expressions for codex drift."""
        fundamental_exprs = [
            # Wave functions in 5D
            {
                "name": "wave_5d",
                "expr": sp.sin(self.vars_5d[0]) * sp.cos(self.vars_5d[1]) * 
                       sp.exp(sp.I * self.vars_5d[2]) * sp.log(1 + sp.Abs(self.vars_5d[3])) *
                       sp.sqrt(1 + self.vars_5d[4]**2),
                "domain": SymbolicDomain.MATHEMATICAL,
                "variables": ['x', 'y', 'z', 't', 's']
            },
            
            # Harmonic oscillator in symbolic space
            {
                "name": "harmonic_symbolic",
                "expr": sp.exp(-self.vars_5d[4]**2/2) * sp.hermite(2, self.vars_5d[4]),
                "domain": SymbolicDomain.QUANTUM,
                "variables": ['s']
            },
            
            # Temporal drift function
            {
                "name": "temporal_drift",
                "expr": self.vars_5d[3] * sp.exp(-self.vars_5d[3]**2/10) * 
                       sp.sin(self.vars_5d[0] + self.vars_5d[1]),
                "domain": SymbolicDomain.TEMPORAL,
                "variables": ['x', 'y', 't']
            },
            
            # Geometric resonance function
            {
                "name": "geometric_resonance",
                "expr": (self.vars_5d[0]**2 + self.vars_5d[1]**2 + self.vars_5d[2]**2) * 
                       sp.exp(-sp.sqrt(self.vars_5d[0]**2 + self.vars_5d[1]**2 + self.vars_5d[2]**2)),
                "domain": SymbolicDomain.GEOMETRIC,
                "variables": ['x', 'y', 'z']
            }
        ]
        
        for expr_def in fundamental_exprs:
            complexity = self._calculate_expression_complexity(expr_def["expr"])
            expr = SymbolicExpression(
                expression=expr_def["expr"],
                domain=expr_def["domain"],
                variables=expr_def["variables"],
                complexity=complexity
            )
            self.expression_cache[expr_def["name"]] = expr
    
    def _calculate_expression_complexity(self, expr: sp.Expr) -> float:
        """Calculate the complexity score of a symbolic expression."""
        # Count operations and nesting depth
        expr_str = str(expr)
        complexity = (
            len(expr_str) * 0.01 +
            expr_str.count('(') * 0.1 +
            expr_str.count('sin') * 0.2 +
            expr_str.count('cos') * 0.2 +
            expr_str.count('exp') * 0.3 +
            expr_str.count('log') * 0.3 +
            expr_str.count('sqrt') * 0.2
        )
        return min(complexity, 10.0)  # Cap at 10.0
    
    def create_symbolic_field(self, 
                            name: str,
                            expressions: List[str],
                            domain: SymbolicDomain = SymbolicDomain.MATHEMATICAL) -> str:
        """Create a new symbolic field from expression strings."""
        field_expressions = []
        
        for expr_str in expressions:
            try:
                # Parse the symbolic expression
                parsed_expr = sp.sympify(expr_str, locals=self.vars_dict)
                
                # Extract variables used
                symbols_in_expr = list(parsed_expr.free_symbols)
                var_names = [str(sym) for sym in symbols_in_expr 
                           if str(sym) in self.vars_dict.keys()]
                
                complexity = self._calculate_expression_complexity(parsed_expr)
                
                sym_expr = SymbolicExpression(
                    expression=parsed_expr,
                    domain=domain,
                    variables=var_names,
                    complexity=complexity
                )
                field_expressions.append(sym_expr)
                
            except Exception as e:
                print(f"Failed to parse expression '{expr_str}': {e}")
                continue
        
        field = SymbolicField(
            expressions=field_expressions,
            field_name=name,
            coherence=self._calculate_field_coherence(field_expressions)
        )
        
        field_id = f"field_{name}_{len(self.symbolic_fields)}"
        self.symbolic_fields[field_id] = field
        
        return field_id
    
    def _calculate_field_coherence(self, expressions: List[SymbolicExpression]) -> float:
        """Calculate coherence measure for a symbolic field."""
        if not expressions:
            return 0.0
        
        # Simple coherence based on variable overlap and complexity variance
        all_vars = set()
        complexities = []
        
        for expr in expressions:
            all_vars.update(expr.variables)
            complexities.append(expr.complexity)
        
        var_overlap = len(all_vars) / (len(expressions) * 5)  # Normalize by max vars
        complexity_variance = np.var(complexities) if len(complexities) > 1 else 0
        
        coherence = max(0, 1.0 - complexity_variance * 0.1) * (1.0 - var_overlap * 0.2)
        return min(coherence, 1.0)
    
    def compute_field_at_vector(self, 
                              field_id: str,
                              vector: ScrollVector) -> Dict[str, complex]:
        """Compute symbolic field values at a specific 5D vector."""
        if field_id not in self.symbolic_fields:
            return {}
        
        field = self.symbolic_fields[field_id]
        results = {}
        
        for i, expr in enumerate(field.expressions):
            try:
                value = expr.evaluate_at_vector(vector)
                results[f"expr_{i}"] = value
            except Exception as e:
                results[f"expr_{i}"] = complex(0, 0)
                print(f"Evaluation error: {e}")
        
        return results
    
    def compute_field_gradient(self, 
                             field_id: str,
                             vector: ScrollVector,
                             delta: float = 1e-6) -> Dict[str, Dict[str, complex]]:
        """Compute the 5D gradient of a symbolic field at a vector."""
        if field_id not in self.symbolic_fields:
            return {}
        
        # Compute partial derivatives numerically
        gradient = {}
        base_values = self.compute_field_at_vector(field_id, vector)
        
        # Partial derivatives in each dimension
        dimensions = ['x', 'y', 'z', 'temporal', 'symbolic']
        
        for dim in dimensions:
            # Create perturbed vector
            perturbed_vector = ScrollVector(
                vector.x + (delta if dim == 'x' else 0),
                vector.y + (delta if dim == 'y' else 0),
                vector.z + (delta if dim == 'z' else 0),
                vector.temporal + (delta if dim == 'temporal' else 0),
                vector.symbolic + (delta if dim == 'symbolic' else 0)
            )
            
            perturbed_values = self.compute_field_at_vector(field_id, perturbed_vector)
            
            # Calculate numerical gradient
            partial_derivatives = {}
            for expr_key in base_values:
                if expr_key in perturbed_values:
                    derivative = (perturbed_values[expr_key] - base_values[expr_key]) / delta
                    partial_derivatives[expr_key] = derivative
                else:
                    partial_derivatives[expr_key] = complex(0, 0)
            
            gradient[f"d_d{dim}"] = partial_derivatives
        
        return gradient
    
    def create_field_from_codex_drift(self, 
                                    codex_field: CodexDriftField,
                                    field_name: str = "codex_derived") -> str:
        """Create a symbolic field derived from a codex drift field."""
        # Extract patterns from the codex drift field
        gradient = codex_field.compute_field_gradient()
        
        # Generate symbolic expressions based on the drift patterns
        expressions = []
        
        # Wave-like expression based on field gradient
        wave_expr = (
            f"sin({gradient.x}*x + {gradient.y}*y) * "
            f"cos({gradient.z}*z) * "
            f"exp(-({gradient.temporal}*t)**2) * "
            f"sqrt(1 + ({gradient.symbolic}*s)**2)"
        )
        expressions.append(wave_expr)
        
        # Resonance expression
        resonance_expr = (
            f"exp(-((x-{gradient.x})**2 + (y-{gradient.y})**2 + (z-{gradient.z})**2)/2) * "
            f"sin({codex_field.drift_coefficient}*t) * "
            f"cos({codex_field.field_strength}*s)"
        )
        expressions.append(resonance_expr)
        
        # Drift expression
        drift_expr = (
            f"({gradient.x}*x + {gradient.y}*y + {gradient.z}*z) * "
            f"exp(-t*{codex_field.temporal_decay}) * "
            f"(1 + s**2)"
        )
        expressions.append(drift_expr)
        
        return self.create_symbolic_field(field_name, expressions, SymbolicDomain.MATHEMATICAL)
    
    def analyze_field_symmetries(self, field_id: str) -> Dict[str, Any]:
        """Analyze symmetries in a symbolic field."""
        if field_id not in self.symbolic_fields:
            return {}
        
        field = self.symbolic_fields[field_id]
        symmetries = {
            "reflection_symmetries": {},
            "rotation_symmetries": {},
            "translation_symmetries": {},
            "scaling_symmetries": {}
        }
        
        # Test sample points for symmetry detection
        test_vectors = [
            ScrollVector(1, 0, 0, 0, 0),
            ScrollVector(0, 1, 0, 0, 0),
            ScrollVector(0, 0, 1, 0, 0),
            ScrollVector(-1, 0, 0, 0, 0),
            ScrollVector(0, -1, 0, 0, 0),
        ]
        
        for vector in test_vectors:
            values = self.compute_field_at_vector(field_id, vector)
            
            # Test reflection symmetry (simple case: negate x coordinate)
            reflected_vector = ScrollVector(-vector.x, vector.y, vector.z, 
                                          vector.temporal, vector.symbolic)
            reflected_values = self.compute_field_at_vector(field_id, reflected_vector)
            
            # Compare values (simplified symmetry check)
            if values and reflected_values:
                symmetry_score = self._compare_field_values(values, reflected_values)
                symmetries["reflection_symmetries"][str(vector.x)] = symmetry_score
        
        return symmetries
    
    def _compare_field_values(self, 
                            values1: Dict[str, complex],
                            values2: Dict[str, complex]) -> float:
        """Compare two sets of field values for similarity."""
        if not values1 or not values2:
            return 0.0
        
        total_diff = 0.0
        count = 0
        
        for key in values1:
            if key in values2:
                diff = abs(values1[key] - values2[key])
                total_diff += diff
                count += 1
        
        if count == 0:
            return 0.0
        
        avg_diff = total_diff / count
        # Convert to similarity score (higher = more similar)
        return max(0.0, 1.0 - avg_diff)
    
    def export_field_analysis(self, field_id: str) -> Dict[str, Any]:
        """Export comprehensive analysis of a symbolic field."""
        if field_id not in self.symbolic_fields:
            return {}
        
        field = self.symbolic_fields[field_id]
        
        analysis = {
            "field_id": field_id,
            "field_name": field.field_name,
            "dimension": field.dimension,
            "coherence": field.coherence,
            "expression_count": len(field.expressions),
            "expressions": [],
            "complexity_stats": {
                "min": min((e.complexity for e in field.expressions), default=0),
                "max": max((e.complexity for e in field.expressions), default=0),
                "avg": sum(e.complexity for e in field.expressions) / len(field.expressions) if field.expressions else 0
            },
            "domain_distribution": {},
            "variable_usage": {}
        }
        
        # Analyze expressions
        for i, expr in enumerate(field.expressions):
            analysis["expressions"].append({
                "index": i,
                "expression_str": str(expr.expression),
                "domain": expr.domain.value,
                "variables": expr.variables,
                "complexity": expr.complexity
            })
            
            # Count domain usage
            domain_key = expr.domain.value
            analysis["domain_distribution"][domain_key] = analysis["domain_distribution"].get(domain_key, 0) + 1
            
            # Count variable usage
            for var in expr.variables:
                analysis["variable_usage"][var] = analysis["variable_usage"].get(var, 0) + 1
        
        return analysis
    
    def get_computer_status(self) -> Dict[str, Any]:
        """Get current symbolic field computer status."""
        return {
            "active_fields": len(self.symbolic_fields),
            "cached_expressions": len(self.expression_cache),
            "fundamental_expressions": len([e for e in self.expression_cache.values()]),
            "total_expressions": sum(len(f.expressions) for f in self.symbolic_fields.values()),
            "field_coherence_avg": sum(f.coherence for f in self.symbolic_fields.values()) / len(self.symbolic_fields) if self.symbolic_fields else 0
        }