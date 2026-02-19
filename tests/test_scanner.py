"""Tests for vendor-risk-monitor."""
import pytest

def test_scanner_import():
    from src.scanner import DependencyScanner
    assert DependencyScanner is not None

def test_ecosystem_enum():
    from src.scanner import Ecosystem
    assert Ecosystem.NPM.value == "npm"