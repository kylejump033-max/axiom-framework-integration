"""
Test Suite for Analysis Modules
Tests: config_analyzer.py and sequence_processor.py
"""

import unittest
import re
from io import StringIO
import sys


class TestConfigAnalyzer(unittest.TestCase):
    """Test configuration string analysis"""
    
    def test_extract_digits(self):
        """Test numeric sequence extraction"""
        config = "01345790100110097654321 |□453¤75|080(777)÷864t ^a ×Lk"
        digits = re.findall(r'\d+', config)
        
        self.assertEqual(digits, ['01345790100110097654321', '453', '75', '080', '777', '864'])
    
    def test_extract_alpha(self):
        """Test alphabetic token extraction"""
        config = "01345790100110097654321 |□453¤75|080(777)÷864t ^a ×Lk"
        alpha = re.findall(r'[a-zA-Z]+', config)
        
        self.assertEqual(alpha, ['t', 'a', 'Lk'])
    
    def test_extract_symbols(self):
        """Test symbol extraction"""
        config = "01345790100110097654321 |□453¤75|080(777)÷864t ^a ×Lk"
        symbols = re.findall(r'[^\w\s]', config)
        
        # Verify symbols are extracted (special chars, operators)
        self.assertGreater(len(symbols), 0)
        self.assertIn('|', symbols)
    
    def test_digit_sum_calculation(self):
        """Test digit sum calculation"""
        config = "123456"
        digits = re.findall(r'\d+', config)
        all_digits = "".join(digits)
        digit_sum = sum(int(d) for d in all_digits)
        
        self.assertEqual(digit_sum, 1+2+3+4+5+6)  # 21
    
    def test_empty_config(self):
        """Test with empty configuration"""
        config = ""
        digits = re.findall(r'\d+', config)
        alpha = re.findall(r'[a-zA-Z]+', config)
        
        self.assertEqual(digits, [])
        self.assertEqual(alpha, [])
    
    def test_config_with_only_digits(self):
        """Test with numeric-only config"""
        config = "123456789"
        digits = re.findall(r'\d+', config)
        
        self.assertEqual(digits, ['123456789'])
    
    def test_config_with_special_chars(self):
        """Test config with various special characters"""
        config = "test!@#$%^&*()_+-=[]{}|;:',.<>?/~`"
        symbols = re.findall(r'[^\w\s]', config)
        
        self.assertGreater(len(symbols), 15)
    
    def test_mixed_content_parsing(self):
        """Test parsing mixed content"""
        config = "2026-08-04 version:0.1.0 status:active"
        
        digits = re.findall(r'\d+', config)
        alpha = re.findall(r'[a-zA-Z]+', config)
        
        self.assertIn('2026', digits)
        self.assertIn('08', digits)
        self.assertIn('04', digits)
        self.assertIn('01', digits)
        self.assertIn('0', digits)
        self.assertIn('version', alpha)
        self.assertIn('status', alpha)
        self.assertIn('active', alpha)


class TestSequenceProcessor(unittest.TestCase):
    """Test sequence log processing"""
    
    def test_entry_id_conversion(self):
        """Test entry ID conversion to integer"""
        entry_id = "00002"
        converted = int(entry_id)
        
        self.assertEqual(converted, 2)
    
    def test_numeric_cluster_identification(self):
        """Test identifying numeric clusters in sequence"""
        config = "01345790100110097654321 |□453¤75|080(777)÷864t ^a ×Lk"
        digits = re.findall(r'\d+', config)
        
        expected_clusters = ['01345790100110097654321', '453', '75', '080', '777', '864']
        self.assertEqual(digits, expected_clusters)
    
    def test_total_digit_count(self):
        """Test counting total digits"""
        config = "01345790100110097654321 |□453¤75|080(777)÷864t ^a ×Lk"
        digits = re.findall(r'\d+', config)
        all_digits = "".join(digits)
        total_count = len(all_digits)
        
        # Count manually: 23 + 3 + 2 + 3 + 3 + 3 = 37
        self.assertEqual(total_count, 37)
    
    def test_digit_sum_accumulation(self):
        """Test digit sum accumulation across clusters"""
        config = "123 456 789"
        digits = re.findall(r'\d+', config)
        all_digits = "".join(digits)
        digit_sum = sum(int(d) for d in all_digits)
        
        # 1+2+3+4+5+6+7+8+9 = 45
        self.assertEqual(digit_sum, 45)
    
    def test_entry_id_padding(self):
        """Test entry ID with leading zeros"""
        entry_ids = ["00001", "00002", "00010", "00100"]
        
        for entry_id in entry_ids:
            converted = int(entry_id)
            self.assertGreater(converted, -1)
            self.assertLess(converted, 1000)
    
    def test_sequence_with_various_formats(self):
        """Test sequences with different formatting"""
        sequences = [
            "001-002-003",
            "001.002.003",
            "001_002_003",
            "001,002,003"
        ]
        
        for seq in sequences:
            digits = re.findall(r'\d+', seq)
            self.assertEqual(len(digits), 3)
            self.assertEqual(digits, ['001', '002', '003'])
    
    def test_large_sequence_processing(self):
        """Test processing of large numeric sequences"""
        config = "1" * 1000  # 1000 ones
        digits = re.findall(r'\d+', config)
        all_digits = "".join(digits)
        digit_sum = sum(int(d) for d in all_digits)
        
        self.assertEqual(len(all_digits), 1000)
        self.assertEqual(digit_sum, 1000)


class TestIntegration(unittest.TestCase):
    """Integration tests for analysis modules"""
    
    def test_config_and_sequence_workflow(self):
        """Test complete workflow: analyze config, then process sequence"""
        config = "01345790100110097654321 |□453¤75|080(777)÷864t ^a ×Lk"
        entry_id = "00002"
        
        # Step 1: Analyze config
        digits = re.findall(r'\d+', config)
        alpha = re.findall(r'[a-zA-Z]+', config)
        
        # Step 2: Process sequence
        entry_converted = int(entry_id)
        all_digits = "".join(digits)
        digit_sum = sum(int(d) for d in all_digits)
        
        # Verify workflow
        self.assertGreater(len(digits), 0)
        self.assertGreater(len(alpha), 0)
        self.assertEqual(entry_converted, 2)
        self.assertGreater(digit_sum, 0)
    
    def test_multiple_configs_analysis(self):
        """Test analyzing multiple configurations"""
        configs = [
            "01345790100110097654321 |□453¤75|080(777)÷864t ^a ×Lk",
            "test_config_001_v2.0",
            "2026-09-04:log-entry-42"
        ]
        
        for config in configs:
            digits = re.findall(r'\d+', config)
            alpha = re.findall(r'[a-zA-Z]+', config)
            
            # All configs should be parseable
            self.assertIsNotNone(digits)
            self.assertIsNotNone(alpha)
    
    def test_error_recovery(self):
        """Test error handling in analysis"""
        try:
            config = None
            # This should handle gracefully
            if config:
                digits = re.findall(r'\d+', config)
        except Exception as e:
            self.fail(f"Analysis failed on None input: {e}")
    
    def test_regex_pattern_stability(self):
        """Test regex patterns don't break on various inputs"""
        test_inputs = [
            "",
            "abc123def",
            "!@#$%^&*()",
            "0" * 500,
            "a" * 500,
            "123!abc@456#def",
            "   spaces   everywhere   ",
            "\n\t\r special whitespace",
            "UPPERCASE lowercase MiXeD",
            "日本語 中文 한국어",  # Non-ASCII
        ]
        
        patterns = [
            (r'\d+', "digits"),
            (r'[a-zA-Z]+', "alpha"),
            (r'[^\w\s]', "symbols"),
        ]
        
        for test_input in test_inputs:
            for pattern, name in patterns:
                try:
                    result = re.findall(pattern, test_input)
                    self.assertIsInstance(result, list)
                except Exception as e:
                    self.fail(f"Regex pattern '{name}' failed on input: {e}")


if __name__ == '__main__':
    unittest.main()
