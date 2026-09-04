"""
Test Suite for Axiom Core Module
Tests: AxiomRecord compilation, JSON serialization, CLI functionality
"""

import unittest
import json
from io import StringIO
import sys
from axiom_core import AxiomRecord, compile_axiom_record


class TestAxiomRecord(unittest.TestCase):
    """Test AxiomRecord dataclass functionality"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.designation = "Perpetual light infinity morning star ii"
        self.statement = "To do onto thyself what thy do on to others."
        self.status = "Synchronized and Logged"
    
    def test_axiom_record_creation(self):
        """Test basic AxiomRecord instantiation"""
        record = AxiomRecord(
            designation=self.designation,
            core_statement=self.statement,
            status=self.status
        )
        self.assertEqual(record.designation, self.designation)
        self.assertEqual(record.core_statement, self.statement)
        self.assertEqual(record.status, self.status)
    
    def test_axiom_record_default_status(self):
        """Test default status value"""
        record = AxiomRecord(
            designation=self.designation,
            core_statement=self.statement
        )
        self.assertEqual(record.status, "Synchronized and Logged")
    
    def test_axiom_record_immutability(self):
        """Test that AxiomRecord is frozen (immutable)"""
        record = AxiomRecord(
            designation=self.designation,
            core_statement=self.statement
        )
        with self.assertRaises(Exception):  # frozen dataclass raises FrozenInstanceError
            record.designation = "Modified"
    
    def test_axiom_record_to_dict(self):
        """Test serialization to dictionary"""
        record = AxiomRecord(
            designation=self.designation,
            core_statement=self.statement,
            status=self.status
        )
        result = record.to_dict()
        
        self.assertIsInstance(result, dict)
        self.assertEqual(result['designation'], self.designation)
        self.assertEqual(result['core_statement'], self.statement)
        self.assertEqual(result['status'], self.status)
    
    def test_axiom_record_to_json(self):
        """Test JSON serialization"""
        record = AxiomRecord(
            designation=self.designation,
            core_statement=self.statement,
            status=self.status
        )
        json_str = json.dumps(record.to_dict(), indent=2)
        parsed = json.loads(json_str)
        
        self.assertEqual(parsed['designation'], self.designation)
        self.assertEqual(parsed['core_statement'], self.statement)
        self.assertEqual(parsed['status'], self.status)


class TestCompileAxiomRecord(unittest.TestCase):
    """Test axiom compilation output"""
    
    def test_compile_axiom_record_format(self):
        """Test compiled output format"""
        record = AxiomRecord(
            designation="Test Axiom",
            core_statement="Test Statement",
            status="Test Status"
        )
        output = compile_axiom_record(record)
        
        # Check for expected components
        self.assertIn("LOGGING PERPETUAL LIGHT AXIOM", output)
        self.assertIn("Test Axiom", output)
        self.assertIn("Test Statement", output)
        self.assertIn("Test Status", output)
        self.assertIn("=" * 50, output)
    
    def test_compile_axiom_record_newlines(self):
        """Test output has proper line breaks"""
        record = AxiomRecord(
            designation="Test",
            core_statement="Test",
            status="Test"
        )
        output = compile_axiom_record(record)
        lines = output.split('\n')
        
        self.assertGreater(len(lines), 5)
    
    def test_compile_axiom_record_special_chars(self):
        """Test handling of special characters in axiom"""
        record = AxiomRecord(
            designation="Test™ Axiom®",
            core_statement="Statement with émojis 🎯",
            status="Status™"
        )
        output = compile_axiom_record(record)
        
        self.assertIn("Test™ Axiom®", output)
        self.assertIn("Statement with émojis 🎯", output)


class TestEdgeCases(unittest.TestCase):
    """Test edge cases and error handling"""
    
    def test_empty_designation(self):
        """Test with empty designation"""
        record = AxiomRecord(
            designation="",
            core_statement="Test",
            status="Test"
        )
        output = compile_axiom_record(record)
        self.assertIn("Designation:", output)
    
    def test_very_long_statement(self):
        """Test with very long statement"""
        long_statement = "A" * 1000
        record = AxiomRecord(
            designation="Test",
            core_statement=long_statement,
            status="Test"
        )
        output = compile_axiom_record(record)
        self.assertIn(long_statement, output)
    
    def test_unicode_characters(self):
        """Test unicode character handling"""
        record = AxiomRecord(
            designation="テスト 测试 δοκιμή",
            core_statement="Тест 테스트",
            status="Test"
        )
        output = compile_axiom_record(record)
        self.assertIn("テスト", output)
        self.assertIn("Тест", output)


if __name__ == '__main__':
    unittest.main()
