#!/usr/bin/env python3
"""
Project Validation Script - Verify all files and basic functionality
Run this to ensure project is set up correctly before presentation
"""

import os
import sys
from pathlib import Path

def check_file_exists(filepath, description):
    """Check if a file exists and print status."""
    if os.path.exists(filepath):
        size = os.path.getsize(filepath)
        print(f"✅ {description:<40} ({size:,} bytes)")
        return True
    else:
        print(f"❌ {description:<40} MISSING")
        return False

def check_file_content(filepath, search_string, description):
    """Check if file contains specific string."""
    try:
        with open(filepath, 'r') as f:
            content = f.read()
            if search_string in content:
                print(f"✅ {description:<40} Found")
                return True
            else:
                print(f"❌ {description:<40} Not found")
                return False
    except:
        print(f"❌ {description:<40} Error reading")
        return False

def test_imports():
    """Test that core modules can be imported."""
    print("\n" + "="*60)
    print("TESTING IMPORTS")
    print("="*60)
    
    try:
        from grid_graph import GridGraph
        print("✅ GridGraph import successful")
    except Exception as e:
        print(f"❌ GridGraph import failed: {e}")
        return False
    
    try:
        from pathfinding import BFS, Dijkstra, AStar
        print("✅ BFS import successful")
        print("✅ Dijkstra import successful")
        print("✅ AStar import successful")
    except Exception as e:
        print(f"❌ Pathfinding import failed: {e}")
        return False
    
    return True

def test_basic_functionality():
    """Test basic functionality."""
    print("\n" + "="*60)
    print("TESTING BASIC FUNCTIONALITY")
    print("="*60)
    
    try:
        from grid_graph import GridGraph
        from pathfinding import BFS
        
        # Create grid
        grid = GridGraph(5, 5)
        print("✅ Grid creation successful")
        
        # Add wall
        grid.set_cell(2, 2, -1)
        print("✅ Wall placement successful")
        
        # Check walkable
        if grid.is_walkable(0, 0) and not grid.is_walkable(2, 2):
            print("✅ Walkability check successful")
        
        # Get neighbors
        neighbors = grid.get_neighbors(2, 2)
        if len(neighbors) == 0:  # Wall has no walkable neighbors
            print("✅ Neighbor retrieval successful")
        
        # Find path
        bfs = BFS(grid)
        path = bfs.find_path((0, 0), (4, 4))
        if path:
            print(f"✅ BFS pathfinding successful (path length: {len(path)})")
        else:
            print("❌ BFS pathfinding failed")
            return False
        
    except Exception as e:
        print(f"❌ Functionality test failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

def verify_project_structure():
    """Verify all required files exist."""
    print("\n" + "="*60)
    print("VERIFYING PROJECT STRUCTURE")
    print("="*60)
    
    base_path = Path(__file__).parent
    
    required_files = {
        "grid_graph.py": "Grid representation module",
        "pathfinding.py": "Pathfinding algorithms",
        "test_pathfinding.py": "Unit tests (24 tests)",
        "demo_ui.py": "Interactive UI",
        "quick_demo.py": "Command-line demos",
        "complexity_analysis.py": "Performance analysis",
        "README.md": "Technical documentation",
        "PRESENTATION_NOTES.md": "Presentation slides (20)",
        "QUICKSTART.md": "Quick start guide",
        "REQUIREMENTS.md": "Setup requirements",
        "PROJECT_SUMMARY.py": "Project summary",
        "INDEX.md": "Project index",
    }
    
    all_exist = True
    for filename, description in required_files.items():
        filepath = base_path / filename
        if not check_file_exists(filepath, description):
            all_exist = False
    
    return all_exist

def count_lines():
    """Count total lines of code."""
    print("\n" + "="*60)
    print("CODE STATISTICS")
    print("="*60)
    
    base_path = Path(__file__).parent
    
    categories = {
        "Core": ["grid_graph.py", "pathfinding.py"],
        "Tests": ["test_pathfinding.py"],
        "Demos": ["quick_demo.py", "demo_ui.py"],
        "Analysis": ["complexity_analysis.py"],
    }
    
    total_lines = 0
    for category, files in categories.items():
        category_lines = 0
        for filename in files:
            filepath = base_path / filename
            try:
                with open(filepath, 'r') as f:
                    lines = len(f.readlines())
                    category_lines += lines
            except:
                pass
        print(f"{category:<15} {category_lines:>5} lines")
        total_lines += category_lines
    
    print(f"{'TOTAL':<15} {total_lines:>5} lines")
    
    return total_lines

def main():
    """Run all validation checks."""
    print("\n")
    print("╔" + "="*58 + "╗")
    print("║" + " PROJECT VALIDATION ".center(58) + "║")
    print("║" + " Shortest Path on Grid - Topic 6 ".center(58) + "║")
    print("╚" + "="*58 + "╝")
    
    results = []
    
    # Check file structure
    print("\n" + "="*60)
    print("CHECKING PROJECT FILES")
    print("="*60)
    results.append(("File Structure", verify_project_structure()))
    
    # Count lines
    count_lines()
    
    # Test imports
    results.append(("Import Tests", test_imports()))
    
    # Test functionality
    results.append(("Functionality", test_basic_functionality()))
    
    # Summary
    print("\n" + "="*60)
    print("VALIDATION SUMMARY")
    print("="*60)
    
    all_passed = True
    for test_name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status} - {test_name}")
        if not passed:
            all_passed = False
    
    print("\n" + "="*60)
    if all_passed:
        print("✅ PROJECT VALIDATION COMPLETE - ALL CHECKS PASSED")
        print("\nProject is ready for:")
        print("  • Unit testing: python test_pathfinding.py")
        print("  • Quick demo: python quick_demo.py")
        print("  • Interactive demo: python demo_ui.py")
        print("  • Presentation in Week 15")
    else:
        print("❌ PROJECT VALIDATION FAILED - SOME CHECKS DID NOT PASS")
        print("Please review errors above and fix issues")
        sys.exit(1)
    print("="*60 + "\n")

if __name__ == '__main__':
    main()
