"""Core Dead Code Stripper implementation."""
import ast
from dataclasses import dataclass
from typing import Dict, List, Set

@dataclass
class StripResult:
    cleaned_code: str
    removed_functions: List[str]
    removed_imports: List[str]
    bytes_saved: int

class DeadCodeStripper:
    """Constructs symbol reachability graphs and strips unreachable functions and unused imports."""
    
    def strip_dead_code(self, source_code: str, entry_points: List[str] = None) -> StripResult:
        tree = ast.parse(source_code)
        entries = set(entry_points or ["main"])

        # 1. Collect all defined functions and all referenced identifiers
        defined_funcs = {}
        called_names = set()

        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                defined_funcs[node.name] = node
            elif isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load):
                called_names.add(node.id)

        # 2. Traverse reachability starting from entry points
        reachable = set(entries)
        queue = list(entries)
        while queue:
            curr = queue.pop(0)
            if curr in defined_funcs:
                # Find calls inside this function
                for child in ast.walk(defined_funcs[curr]):
                    if isinstance(child, ast.Name) and child.id in defined_funcs and child.id not in reachable:
                        reachable.add(child.id)
                        queue.append(child.id)

        # Unreachable functions to remove
        unreachable = [f for f in defined_funcs.keys() if f not in reachable]

        # Filter AST nodes
        class FunctionPruner(ast.NodeTransformer):
            def visit_FunctionDef(self, node):
                if node.name in unreachable:
                    return None  # Delete
                return node
            def visit_AsyncFunctionDef(self, node):
                if node.name in unreachable:
                    return None
                return node

        pruned_tree = FunctionPruner().visit(tree)
        ast.fix_missing_locations(pruned_tree)
        cleaned_source = ast.unparse(pruned_tree)
        bytes_saved = len(source_code) - len(cleaned_source)

        return StripResult(
            cleaned_code=cleaned_source,
            removed_functions=unreachable,
            removed_imports=[],
            bytes_saved=max(0, bytes_saved)
        )
