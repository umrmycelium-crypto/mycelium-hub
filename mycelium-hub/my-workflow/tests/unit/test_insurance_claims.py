"""Unit tests for the insurance claims workflow.

This module tests:
- Pydantic models validation
- Workflow routing logic
- Severity aggregation
- Model serialization/deserialization
"""

import json
from enum import Enum

import pytest
from pydantic import ValidationError

from src.examples.insurance_claims.models import (
    ClaimInput,
    ClaimTriageOutput,
    ConsistencyCheck,
    DamageLabel,
    FraudRiskAssessment,
    PhotoAnalysisResult,
    SeverityClassification,
    SeverityLevel,
    TriageReport,
)
from src.examples.insurance_claims.workflow import (
    InsuranceClaimsTriageWorkflow,
    _aggregate_severity,
    _route,
)


# =============================================================================
# DamageLabel Enum Tests
# =============================================================================


class TestDamageLabel:
    """Tests for DamageLabel enum."""

    def test_all_labels_exist(self) -> None:
        """Test that all expected damage labels exist."""
        expected_labels = ["none", "minor", "moderate", "severe", "totaled"]
        for label in expected_labels:
            assert hasattr(DamageLabel, label.upper())

    def test_label_values(self) -> None:
        """Test that label values match expected strings."""
        assert DamageLabel.NONE.value == "none"
        assert DamageLabel.MINOR.value == "minor"
        assert DamageLabel.MODERATE.value == "moderate"
        assert DamageLabel.SEVERE.value == "severe"
        assert DamageLabel.TOTALED.value == "totaled"

    def test_label_ordering(self) -> None:
        """Test that labels maintain severity ordering."""
        # Severity increases in this order - verify the enum values are in order
        expected_order = ["none", "minor", "moderate", "severe", "totaled"]
        for i, label in enumerate(DamageLabel):
            assert label.value == expected_order[i]


# =============================================================================
# SeverityLevel Enum Tests
# =============================================================================


class TestSeverityLevel:
    """Tests for SeverityLevel enum."""

    def test_all_levels_exist(self) -> None:
        """Test that all expected severity levels exist."""
        expected_levels = ["low", "medium", "high"]
        for level in expected_levels:
            assert hasattr(SeverityLevel, level.upper())

    def test_level_values(self) -> None:
        """Test that level values match expected strings."""
        assert SeverityLevel.LOW.value == "low"
        assert SeverityLevel.MEDIUM.value == "medium"
        assert SeverityLevel.HIGH.value == "high"


# =============================================================================
# ClaimInput Model Tests
# =============================================================================


class TestClaimInput:
    """Tests for ClaimInput model."""

    def test_required_fields(self) -> None:
        """Test that required fields are enforced."""
        with pytest.raises(ValidationError):
            ClaimInput()  # Missing required fields

    def test_valid_input(self) -> None:
        """Test valid claim input."""
        input_data = ClaimInput(
            claim_id="CLM-001",
            claimant_name="John Doe",
            description="Car accident",
            photos=["file:///path/to/photo.jpg"],
        )
        assert input_data.claim_id == "CLM-001"
        assert input_data.claimant_name == "John Doe"
        assert len(input_data.photos) == 1

    def test_default_photos(self) -> None:
        """Test that photos defaults to empty list."""
        input_data = ClaimInput(
            claim_id="CLM-001",
            claimant_name="John Doe",
            description="Car accident",
        )
        assert input_data.photos == []

    def test_min_photos_validation(self) -> None:
        """Test that photos list must have at least 1 item when provided."""
        # The photos field has min_length=1, so empty list is not allowed
        with pytest.raises(ValidationError):
            ClaimInput(
                claim_id="CLM-001",
                claimant_name="John Doe",
                description="Car accident",
                photos=[],
            )

    def test_serialization(self) -> None:
        """Test JSON serialization."""
        input_data = ClaimInput(
            claim_id="CLM-001",
            claimant_name="John Doe",
            description="Car accident",
            photos=["file:///path/to/photo1.jpg", "file:///path/to/photo2.jpg"],
        )
        json_str = input_data.model_dump_json()
        parsed = json.loads(json_str)
        assert parsed["claim_id"] == "CLM-001"
        assert parsed["claimant_name"] == "John Doe"
        assert len(parsed["photos"]) == 2


# =============================================================================
# PhotoAnalysisResult Model Tests
# =============================================================================


class TestPhotoAnalysisResult:
    """Tests for PhotoAnalysisResult model."""

    def test_valid_result(self) -> None:
        """Test valid photo analysis result."""
        result = PhotoAnalysisResult(
            photo_uri="file:///path/to/photo.jpg",
            damage_label=DamageLabel.SEVERE,
            damage_description="Major damage to front bumper",
            confidence=0.95,
        )
        assert result.damage_label == DamageLabel.SEVERE
        assert result.confidence == 0.95

    def test_confidence_bounds(self) -> None:
        """Test that confidence is bounded between 0 and 1."""
        # Valid confidence values (confidence is required, not optional)
        PhotoAnalysisResult(
            photo_uri="test",
            damage_label=DamageLabel.NONE,
            damage_description="None",
            confidence=0.0,
        )
        PhotoAnalysisResult(
            photo_uri="test",
            damage_label=DamageLabel.NONE,
            damage_description="None",
            confidence=1.0,
        )
        PhotoAnalysisResult(
            photo_uri="test",
            damage_label=DamageLabel.NONE,
            damage_description="None",
            confidence=0.5,
        )

    def test_confidence_out_of_bounds(self) -> None:
        """Test that confidence outside [0, 1] raises validation error."""
        with pytest.raises(ValidationError):
            PhotoAnalysisResult(
                photo_uri="test",
                damage_label=DamageLabel.NONE,
                damage_description="None",
                confidence=-0.1,
            )
        
        with pytest.raises(ValidationError):
            PhotoAnalysisResult(
                photo_uri="test",
                damage_label=DamageLabel.NONE,
                damage_description="None",
                confidence=1.5,
            )

    def test_confidence_required(self) -> None:
        """Test that confidence is a required field."""
        # confidence is required (no default), so omitting it should raise error
        with pytest.raises(ValidationError):
            PhotoAnalysisResult(
                photo_uri="test",
                damage_label=DamageLabel.NONE,
                damage_description="None",
            )
        # Let's check the actual model definition


# =============================================================================
# ConsistencyCheck Model Tests
# =============================================================================


class TestConsistencyCheck:
    """Tests for ConsistencyCheck model."""

    def test_valid_consistency_check(self) -> None:
        """Test valid consistency check."""
        check = ConsistencyCheck(
            consistent=True,
            discrepancies=[],
            summary="Photos match description",
        )
        assert check.consistent is True
        assert len(check.discrepancies) == 0

    def test_inconsistent_check(self) -> None:
        """Test inconsistent check with discrepancies."""
        check = ConsistencyCheck(
            consistent=False,
            discrepancies=["Photo shows severe damage", "Description says minor"],
            summary="Mismatch between photos and description",
        )
        assert check.consistent is False
        assert len(check.discrepancies) == 2

    def test_default_discrepancies(self) -> None:
        """Test default discrepancies is empty list."""
        check = ConsistencyCheck(
            consistent=True,
            summary="All good",
        )
        assert check.discrepancies == []


# =============================================================================
# FraudRiskAssessment Model Tests
# =============================================================================


class TestFraudRiskAssessment:
    """Tests for FraudRiskAssessment model."""

    def test_valid_assessment(self) -> None:
        """Test valid fraud risk assessment."""
        assessment = FraudRiskAssessment(
            fraud_risk_score=0.75,
            fraud_indicators=["Inconsistent description", "Suspicious timing"],
            reasoning="Multiple red flags detected",
        )
        assert assessment.fraud_risk_score == 0.75
        assert len(assessment.fraud_indicators) == 2

    def test_score_bounds(self) -> None:
        """Test that fraud_risk_score is bounded between 0 and 1."""
        FraudRiskAssessment(
            fraud_risk_score=0.0,
            fraud_indicators=[],
            reasoning="Low risk",
        )
        FraudRiskAssessment(
            fraud_risk_score=1.0,
            fraud_indicators=["All flags"],
            reasoning="High risk",
        )

    def test_score_out_of_bounds(self) -> None:
        """Test that score outside [0, 1] raises validation error."""
        with pytest.raises(ValidationError):
            FraudRiskAssessment(
                fraud_risk_score=-0.1,
                fraud_indicators=[],
                reasoning="Test",
            )
        
        with pytest.raises(ValidationError):
            FraudRiskAssessment(
                fraud_risk_score=1.5,
                fraud_indicators=[],
                reasoning="Test",
            )

    def test_default_fraud_indicators(self) -> None:
        """Test default fraud_indicators is empty list."""
        assessment = FraudRiskAssessment(
            fraud_risk_score=0.5,
            reasoning="Test",
        )
        assert assessment.fraud_indicators == []


# =============================================================================
# Severity Classification Tests
# =============================================================================


class TestSeverityClassification:
    """Tests for SeverityClassification model."""

    def test_valid_classification(self) -> None:
        """Test valid severity classification."""
        classification = SeverityClassification(
            severity=SeverityLevel.HIGH,
            routing_queue="full-investigation",
            rationale="Severity is high",
        )
        assert classification.severity == SeverityLevel.HIGH
        assert classification.routing_queue == "full-investigation"


# =============================================================================
# TriageReport Model Tests
# =============================================================================


class TestTriageReport:
    """Tests for TriageReport model."""

    def test_valid_report(self) -> None:
        """Test valid triage report."""
        report = TriageReport(
            claim_id="CLM-001",
            claimant_name="John Doe",
            severity=SeverityLevel.MEDIUM,
            routing_queue="adjuster-review",
            fraud_risk_score=0.3,
            fraud_indicators=["Minor inconsistency"],
            photo_findings=[{"photo": "photo1", "damage": "minor"}],
            consistency_check={"consistent": True},
            reasoning="Based on analysis",
            cited_evidence=["photo1", "photo2"],
        )
        assert report.claim_id == "CLM-001"
        assert report.severity == SeverityLevel.MEDIUM


# =============================================================================
# ClaimTriageOutput Model Tests
# =============================================================================


class TestClaimTriageOutput:
    """Tests for ClaimTriageOutput model."""

    def test_valid_output(self) -> None:
        """Test valid claim triage output."""
        # Create a minimal report first
        report = TriageReport(
            claim_id="CLM-001",
            claimant_name="John Doe",
            severity=SeverityLevel.LOW,
            routing_queue="fast-track",
            fraud_risk_score=0.1,
            fraud_indicators=[],
            photo_findings=[],
            consistency_check={},
            reasoning="",
            cited_evidence=[],
        )
        
        output = ClaimTriageOutput(
            claim_id="CLM-001",
            routing_decision="fast-track",
            severity=SeverityLevel.LOW,
            fraud_risk_score=0.1,
            report=report,
        )
        assert output.claim_id == "CLM-001"
        assert output.routing_decision == "fast-track"


# =============================================================================
# Workflow Helper Function Tests
# =============================================================================


class TestAggregateSeverity:
    """Tests for _aggregate_severity helper function."""

    def test_no_damage(self) -> None:
        """Test aggregation with no damage."""
        results = [
            PhotoAnalysisResult(
                photo_uri="photo1",
                damage_label=DamageLabel.NONE,
                damage_description="No damage",
                confidence=1.0,
            )
        ]
        severity = _aggregate_severity(results)
        assert severity == SeverityLevel.LOW

    def test_minor_damage(self) -> None:
        """Test aggregation with minor damage."""
        results = [
            PhotoAnalysisResult(
                photo_uri="photo1",
                damage_label=DamageLabel.MINOR,
                damage_description="Minor scratches",
                confidence=0.9,
            )
        ]
        severity = _aggregate_severity(results)
        assert severity == SeverityLevel.LOW

    def test_moderate_damage(self) -> None:
        """Test aggregation with moderate damage."""
        results = [
            PhotoAnalysisResult(
                photo_uri="photo1",
                damage_label=DamageLabel.MODERATE,
                damage_description="Dent",
                confidence=0.8,
            )
        ]
        severity = _aggregate_severity(results)
        assert severity == SeverityLevel.MEDIUM

    def test_severe_damage(self) -> None:
        """Test aggregation with severe damage."""
        results = [
            PhotoAnalysisResult(
                photo_uri="photo1",
                damage_label=DamageLabel.SEVERE,
                damage_description="Structural damage",
                confidence=0.95,
            )
        ]
        severity = _aggregate_severity(results)
        assert severity == SeverityLevel.HIGH

    def test_totaled_damage(self) -> None:
        """Test aggregation with totaled damage."""
        results = [
            PhotoAnalysisResult(
                photo_uri="photo1",
                damage_label=DamageLabel.TOTALED,
                damage_description="Total loss",
                confidence=0.99,
            )
        ]
        severity = _aggregate_severity(results)
        assert severity == SeverityLevel.HIGH

    def test_mixed_damage_highest_wins(self) -> None:
        """Test that highest severity wins in mixed results."""
        results = [
            PhotoAnalysisResult(
                photo_uri="photo1",
                damage_label=DamageLabel.MINOR,
                damage_description="Minor",
                confidence=0.8,
            ),
            PhotoAnalysisResult(
                photo_uri="photo2",
                damage_label=DamageLabel.TOTALED,
                damage_description="Total loss",
                confidence=0.99,
            ),
        ]
        severity = _aggregate_severity(results)
        assert severity == SeverityLevel.HIGH

    def test_multiple_high_severity(self) -> None:
        """Test with multiple high severity indicators."""
        results = [
            PhotoAnalysisResult(
                photo_uri="photo1",
                damage_label=DamageLabel.SEVERE,
                damage_description="Severe",
                confidence=0.95,
            ),
            PhotoAnalysisResult(
                photo_uri="photo2",
                damage_label=DamageLabel.TOTALED,
                damage_description="Total loss",
                confidence=0.99,
            ),
        ]
        severity = _aggregate_severity(results)
        assert severity == SeverityLevel.HIGH

    def test_empty_results(self) -> None:
        """Test with empty results list."""
        severity = _aggregate_severity([])
        assert severity == SeverityLevel.LOW


class TestRoute:
    """Tests for _route helper function."""

    def test_low_severity_routes_to_fast_track(self) -> None:
        """Test low severity routes to fast-track."""
        queue = _route(SeverityLevel.LOW)
        assert queue == "fast-track"

    def test_medium_severity_routes_to_adjuster_review(self) -> None:
        """Test medium severity routes to adjuster-review."""
        queue = _route(SeverityLevel.MEDIUM)
        assert queue == "adjuster-review"

    def test_high_severity_routes_to_full_investigation(self) -> None:
        """Test high severity routes to full-investigation."""
        queue = _route(SeverityLevel.HIGH)
        assert queue == "full-investigation"


# =============================================================================
# Model Serialization Round-trip Tests
# =============================================================================


class TestModelRoundtrip:
    """Tests for model serialization and deserialization."""

    def test_claim_input_roundtrip(self) -> None:
        """Test ClaimInput can be serialized and deserialized."""
        original = ClaimInput(
            claim_id="CLM-001",
            claimant_name="John Doe",
            description="Test claim",
            photos=["file:///path/to/photo.jpg"],
        )
        json_str = original.model_dump_json()
        restored = ClaimInput.model_validate_json(json_str)
        assert restored == original

    def test_photo_analysis_result_roundtrip(self) -> None:
        """Test PhotoAnalysisResult roundtrip."""
        original = PhotoAnalysisResult(
            photo_uri="file:///path/to/photo.jpg",
            damage_label=DamageLabel.SEVERE,
            damage_description="Major damage",
            confidence=0.95,
        )
        json_str = original.model_dump_json()
        restored = PhotoAnalysisResult.model_validate_json(json_str)
        assert restored == original

    def test_severity_level_roundtrip(self) -> None:
        """Test SeverityLevel enum roundtrip."""
        for level in SeverityLevel:
            json_str = json.dumps({"severity": level.value})
            parsed = json.loads(json_str)
            restored = SeverityLevel(parsed["severity"])
            assert restored == level


# =============================================================================
# Workflow Class Tests
# =============================================================================


class TestInsuranceClaimsTriageWorkflow:
    """Tests for the InsuranceClaimsTriageWorkflow class."""

    def test_workflow_has_entrypoint(self) -> None:
        """Test that workflow has the entrypoint method."""
        workflow = InsuranceClaimsTriageWorkflow()
        assert hasattr(workflow, "run")

    def test_workflow_definition_metadata(self) -> None:
        """Test workflow metadata is properly defined."""
        from mistralai.workflows.core.definition.workflow_definition import (
            get_workflow_definition,
        )
        
        workflow_class = InsuranceClaimsTriageWorkflow
        definition = get_workflow_definition(workflow_class)
        
        assert definition.name == "insurance-claims-triage"
        # The spec object might have different attribute names
        # Check that the definition has the expected name
        assert hasattr(definition, 'name')


# =============================================================================
# Edge Case Tests
# =============================================================================


class TestEdgeCases:
    """Edge case tests for insurance claims models."""

    def test_photos_with_multiple_schemas(self) -> None:
        """Test photos with various URI schemes."""
        claim = ClaimInput(
            claim_id="CLM-001",
            claimant_name="John",
            description="Test",
            photos=[
                "file:///local/path",
                "https://example.com/remote.jpg",
                "s3://bucket/key.jpg",
            ],
        )
        assert len(claim.photos) == 3

    def test_long_description(self) -> None:
        """Test with very long description."""
        long_desc = "A" * 10000
        claim = ClaimInput(
            claim_id="CLM-001",
            claimant_name="John",
            description=long_desc,
        )
        assert len(claim.description) == 10000

    def test_special_characters_in_fields(self) -> None:
        """Test with special characters in all fields."""
        claim = ClaimInput(
            claim_id="CLM-001<>&\"'",
            claimant_name="José <O'Brien>",
            description="Accident at 5th & Main (test)\nNew line",
        )
        assert claim.claim_id == "CLM-001<>&\"'"
        assert claim.claimant_name == "José <O'Brien>"
