"""
Comprehensive Test Runner & Bug Check Report
Executes all unit tests and generates stability report
"""

import unittest
import sys
import json
from datetime import datetime
from io import StringIO


class TestRunnerWithReport:
    """Executes tests and generates comprehensive bug check report"""
    
    def __init__(self):
        self.results = {
            "timestamp": datetime.now().isoformat(),
            "test_suites": [],
            "summary": {
                "total_tests": 0,
                "passed": 0,
                "failed": 0,
                "errors": 0,
                "skipped": 0,
                "success_rate": 0.0
            },
            "stability_status": "UNKNOWN",
            "breaking_issues": [],
            "warnings": [],
            "recommendations": []
        }
    
    def run_tests(self):
        """Execute all unit tests"""
        
        # Discover and run all tests
        loader = unittest.TestLoader()
        suite = loader.discover('tests', pattern='test_*.py')
        
        # Run with custom result handler
        stream = StringIO()
        runner = unittest.TextTestRunner(stream=stream, verbosity=2)
        result = runner.run(suite)
        
        # Process results
        self._process_results(result, stream.getvalue())
        
        return result
    
    def _process_results(self, result, output):
        """Process test results into report"""
        
        total = result.testsRun
        failed = len(result.failures)
        errors = len(result.errors)
        skipped = len(result.skipped)
        passed = total - failed - errors - skipped
        
        self.results["summary"]["total_tests"] = total
        self.results["summary"]["passed"] = passed
        self.results["summary"]["failed"] = failed
        self.results["summary"]["errors"] = errors
        self.results["summary"]["skipped"] = skipped
        
        if total > 0:
            self.results["summary"]["success_rate"] = round((passed / total) * 100, 2)
        
        # Determine stability status
        if errors > 0:
            self.results["stability_status"] = "CRITICAL - CODE FRACTURE DETECTED"
            for test, traceback in result.errors:
                self.results["breaking_issues"].append({
                    "test": str(test),
                    "type": "ERROR",
                    "details": traceback
                })
        elif failed > 0:
            self.results["stability_status"] = "UNSTABLE - TEST FAILURES"
            for test, traceback in result.failures:
                self.results["breaking_issues"].append({
                    "test": str(test),
                    "type": "FAILURE",
                    "details": traceback
                })
        elif passed == total:
            self.results["stability_status"] = "STABLE - ALL TESTS PASSED"
        else:
            self.results["stability_status"] = "WARNING - INCOMPLETE TESTING"
        
        # Add recommendations
        self._generate_recommendations()
    
    def _generate_recommendations(self):
        """Generate recommendations based on test results"""
        summary = self.results["summary"]
        
        if summary["success_rate"] == 100:
            self.results["recommendations"].append(
                "✓ Code is production-ready. All tests passing."
            )
            self.results["recommendations"].append(
                "✓ Safe to deploy to main branch."
            )
        elif summary["success_rate"] >= 90:
            self.results["recommendations"].append(
                "⚠ Code is mostly stable (90%+ pass rate)."
            )
            self.results["recommendations"].append(
                "→ Review failing tests before deployment."
            )
        elif summary["success_rate"] >= 70:
            self.results["recommendations"].append(
                "⚠ Code needs review (70-89% pass rate)."
            )
            self.results["recommendations"].append(
                "→ Fix failing tests before merging to main."
            )
        else:
            self.results["recommendations"].append(
                "✗ Code is NOT STABLE - Major issues detected."
            )
            self.results["recommendations"].append(
                "→ DO NOT DEPLOY. Debug all failing tests."
            )
    
    def generate_report(self):
        """Generate human-readable bug check report"""
        
        report = []
        report.append("\n" + "="*60)
        report.append("AXIOM FRAMEWORK - BUG CHECK & STABILITY REPORT")
        report.append("="*60)
        report.append(f"Generated: {self.results['timestamp']}\n")
        
        # Overall Status
        report.append(f"STABILITY STATUS: {self.results['stability_status']}")
        report.append("")
        
        # Summary Statistics
        summary = self.results["summary"]
        report.append("TEST SUMMARY:")
        report.append(f"  Total Tests Run:  {summary['total_tests']}")
        report.append(f"  Passed:           {summary['passed']} ✓")
        report.append(f"  Failed:           {summary['failed']} ✗")
        report.append(f"  Errors:           {summary['errors']} ⚠")
        report.append(f"  Skipped:          {summary['skipped']} ⊘")
        report.append(f"  Success Rate:     {summary['success_rate']}%")
        report.append("")
        
        # Breaking Issues
        if self.results["breaking_issues"]:
            report.append("BREAKING ISSUES DETECTED:")
            for i, issue in enumerate(self.results["breaking_issues"], 1):
                report.append(f"\n  [{i}] {issue['type']}: {issue['test']}")
                report.append(f"      {issue['details'][:200]}...")
        else:
            report.append("✓ NO BREAKING ISSUES DETECTED")
        
        report.append("")
        
        # Recommendations
        if self.results["recommendations"]:
            report.append("RECOMMENDATIONS:")
            for rec in self.results["recommendations"]:
                report.append(f"  {rec}")
        
        report.append("\n" + "="*60)
        report.append("CODE STABILITY ASSESSMENT:")
        report.append("="*60)
        
        if summary["success_rate"] == 100:
            status_text = "✓ STABLE - READY FOR DEPLOYMENT"
        elif summary["success_rate"] >= 90:
            status_text = "⚠ MOSTLY STABLE - REVIEW NEEDED"
        elif summary["success_rate"] >= 70:
            status_text = "⚠ UNSTABLE - REQUIRES FIXES"
        else:
            status_text = "✗ CRITICAL - DO NOT DEPLOY"
        
        report.append(f"\n  {status_text}")
        report.append(f"  Pass Rate: {summary['success_rate']}%")
        report.append(f"  Fractures: {len(self.results['breaking_issues'])}")
        report.append("\n" + "="*60 + "\n")
        
        return "\n".join(report)
    
    def generate_json_report(self):
        """Generate JSON format report"""
        return json.dumps(self.results, indent=2)


def main():
    """Main test execution"""
    
    print("Starting comprehensive bug check and stability test...\n")
    
    runner = TestRunnerWithReport()
    result = runner.run_tests()
    
    # Generate and print report
    report = runner.generate_report()
    print(report)
    
    # Also save JSON report
    json_report = runner.generate_json_report()
    
    try:
        with open('test_report.json', 'w') as f:
            f.write(json_report)
        print("✓ JSON report saved to: test_report.json")
    except Exception as e:
        print(f"⚠ Could not save JSON report: {e}")
    
    # Exit with appropriate code
    if result.wasSuccessful():
        print("\n✓ All tests passed! Code is stable.")
        return 0
    else:
        print(f"\n✗ Tests failed! {len(result.failures)} failures, {len(result.errors)} errors")
        return 1


if __name__ == '__main__':
    sys.exit(main())
