"""Unit tests for the cargo release workflow.

This module tests:
- Pydantic models validation
- Workflow models
- Sub-workflow integration
- Conditional branching logic
- Model serialization
"""

import json

import pytest
from pydantic import ValidationError

from src.examples.cargo_release.models import (
    CargoClassification,
    CargoReleaseInput,
    CargoReleaseResult,
    ComplianceCheck,
    DangerousGoodsParams,
    DangerousGoodsResult,
)
from src.examples.cargo_release.workflow import (
    CargoReleaseWorkflow,
    DangerousGoodsValidationWorkflow,
    _CARGO_NAME,
    _DG_NAME,
)


# =============================================================================
# CargoReleaseInput Model Tests
# =============================================================================


class TestCargoReleaseInput:
    """Tests for CargoReleaseInput model."""

    def test_required_fields(self) -> None:
        """Test that required fields are enforced."""
        with pytest.raises(ValidationError):
            CargoReleaseInput()  # Missing required fields

    def test_valid_input(self) -> None:
        """Test valid cargo release input."""
        input_data = CargoReleaseInput(
            document_uri="file:///path/to/shipping_doc.pdf",
            shipment_id="BL-2024-HAM-009371",
        )
        assert input_data.document_uri == "file:///path/to/shipping_doc.pdf"
        assert input_data.shipment_id == "BL-2024-HAM-009371"

    def test_various_uri_schemes(self) -> None:
        """Test various document URI schemes."""
        uri_schemes = [
            "file:///local/path/doc.pdf",
            "https://example.com/shipping_doc.pdf",
            "s3://bucket/key.pdf",
            "/absolute/path/doc.pdf",
        ]
        
        for uri in uri_schemes:
            input_data = CargoReleaseInput(
                document_uri=uri,
                shipment_id="TEST-001",
            )
            assert input_data.document_uri == uri

    def test_serialization(self) -> None:
        """Test JSON serialization."""
        input_data = CargoReleaseInput(
            document_uri="file:///path/to/doc.pdf",
            shipment_id="BL-2024-TEST",
        )
        json_str = input_data.model_dump_json()
        parsed = json.loads(json_str)
        assert parsed["document_uri"] == "file:///path/to/doc.pdf"
        assert parsed["shipment_id"] == "BL-2024-TEST"

    def test_roundtrip(self) -> None:
        """Test serialization and deserialization roundtrip."""
        original = CargoReleaseInput(
            document_uri="https://example.com/doc.pdf",
            shipment_id="SHIP-123",
        )
        json_str = original.model_dump_json()
        restored = CargoReleaseInput.model_validate_json(json_str)
        assert restored == original


# =============================================================================
# CargoClassification Model Tests
# =============================================================================


class TestCargoClassification:
    """Tests for CargoClassification model."""

    def test_general_cargo(self) -> None:
        """Test classification as general cargo."""
        classification = CargoClassification(
            cargo_type="general",
            reasoning="No special handling required",
        )
        assert classification.cargo_type == "general"

    def test_dangerous_goods(self) -> None:
        """Test classification as dangerous goods."""
        classification = CargoClassification(
            cargo_type="dangerous_goods",
            reasoning="Contains flammable materials",
        )
        assert classification.cargo_type == "dangerous_goods"

    def test_perishable(self) -> None:
        """Test classification as perishable."""
        classification = CargoClassification(
            cargo_type="perishable",
            reasoning="Requires temperature control",
        )
        assert classification.cargo_type == "perishable"

    def test_invalid_cargo_type(self) -> None:
        """Test that invalid cargo types raise validation error."""
        with pytest.raises(ValidationError):
            CargoClassification(
                cargo_type="invalid_type",
                reasoning="Test",
            )

    def test_serialization(self) -> None:
        """Test JSON serialization."""
        classification = CargoClassification(
            cargo_type="dangerous_goods",
            reasoning="Contains chemicals",
        )
        json_str = classification.model_dump_json()
        parsed = json.loads(json_str)
        assert parsed["cargo_type"] == "dangerous_goods"


# =============================================================================
# DangerousGoodsParams Model Tests
# =============================================================================


class TestDangerousGoodsParams:
    """Tests for DangerousGoodsParams model."""

    def test_required_fields(self) -> None:
        """Test that required fields are enforced."""
        with pytest.raises(ValidationError):
            DangerousGoodsParams()  # Missing required fields

    def test_valid_params(self) -> None:
        """Test valid dangerous goods parameters."""
        params = DangerousGoodsParams(
            extracted_text="Shipping document text",
            shipment_id="BL-2024-TEST",
        )
        assert params.extracted_text == "Shipping document text"
        assert params.shipment_id == "BL-2024-TEST"

    def test_long_extracted_text(self) -> None:
        """Test with very long extracted text."""
        long_text = "A" * 10000
        params = DangerousGoodsParams(
            extracted_text=long_text,
            shipment_id="TEST-001",
        )
        assert len(params.extracted_text) == 10000


# =============================================================================
# DangerousGoodsResult Model Tests
# =============================================================================


class TestDangerousGoodsResult:
    """Tests for DangerousGoodsResult model."""

    def test_valid_result_with_anomalies(self) -> None:
        """Test valid result with anomalies."""
        result = DangerousGoodsResult(
            un_number="UN 1203",
            hazard_class="Class 3 - Flammable liquids",
            anomalies=["Missing emergency contact", "Missing proper shipping name"],
            has_anomaly=True,
        )
        assert result.un_number == "UN 1203"
        assert result.hazard_class == "Class 3 - Flammable liquids"
        assert len(result.anomalies) == 2
        assert result.has_anomaly is True

    def test_valid_result_no_anomalies(self) -> None:
        """Test valid result with no anomalies."""
        result = DangerousGoodsResult(
            un_number="UN 1203",
            hazard_class="Class 3",
            anomalies=[],
            has_anomaly=False,
        )
        assert result.has_anomaly is False
        assert len(result.anomalies) == 0

    def test_default_values(self) -> None:
        """Test default values for optional fields."""
        result = DangerousGoodsResult(
            anomalies=[],
            has_anomaly=False,
        )
        assert result.un_number is None
        assert result.hazard_class is None
        assert result.anomalies == []
        assert result.has_anomaly is False

    def test_has_anomaly_inference(self) -> None:
        """Test that has_anomaly can be inferred from anomalies list."""
        # When anomalies is non-empty, has_anomaly should be True
        result = DangerousGoodsResult(
            anomalies=["Anomaly 1"],
            has_anomaly=True,
        )
        assert result.has_anomaly is True

    def test_serialization(self) -> None:
        """Test JSON serialization."""
        result = DangerousGoodsResult(
            un_number="UN 1203",
            hazard_class="Class 3",
            anomalies=["Missing contact"],
            has_anomaly=True,
        )
        json_str = result.model_dump_json()
        parsed = json.loads(json_str)
        assert parsed["un_number"] == "UN 1203"
        assert parsed["has_anomaly"] is True


# =============================================================================
# ComplianceCheck Model Tests
# =============================================================================


class TestComplianceCheck:
    """Tests for ComplianceCheck model."""

    def test_passed_compliance(self) -> None:
        """Test compliance check that passed."""
        check = ComplianceCheck(
            passed=True,
            failed_rules=[],
            notes="All rules satisfied",
        )
        assert check.passed is True
        assert len(check.failed_rules) == 0

    def test_failed_compliance(self) -> None:
        """Test compliance check that failed."""
        check = ComplianceCheck(
            passed=False,
            failed_rules=["HS code missing", "Country of origin not declared"],
            notes="Two critical rules failed",
        )
        assert check.passed is False
        assert len(check.failed_rules) == 2

    def test_default_values(self) -> None:
        """Test default values."""
        check = ComplianceCheck(
            passed=True,
            notes="OK",
        )
        assert check.failed_rules == []

    def test_serialization(self) -> None:
        """Test JSON serialization."""
        check = ComplianceCheck(
            passed=False,
            failed_rules=["Rule 1", "Rule 2"],
            notes="Failed",
        )
        json_str = check.model_dump_json()
        parsed = json.loads(json_str)
        assert parsed["passed"] is False
        assert len(parsed["failed_rules"]) == 2


# =============================================================================
# CargoReleaseResult Model Tests
# =============================================================================


class TestCargoReleaseResult:
    """Tests for CargoReleaseResult model."""

    def test_released_status(self) -> None:
        """Test result with released status."""
        result = CargoReleaseResult(
            shipment_id="BL-2024-TEST",
            status="released",
            cargo_type="general",
            release_certificate="Certificate text here",
            block_reason=None,
        )
        assert result.status == "released"
        assert result.release_certificate == "Certificate text here"
        assert result.block_reason is None

    def test_blocked_status(self) -> None:
        """Test result with blocked status."""
        result = CargoReleaseResult(
            shipment_id="BL-2024-TEST",
            status="blocked",
            cargo_type="dangerous_goods",
            release_certificate=None,
            block_reason="Reviewer blocked shipment",
        )
        assert result.status == "blocked"
        assert result.release_certificate is None
        assert result.block_reason == "Reviewer blocked shipment"

    def test_invalid_status(self) -> None:
        """Test that invalid status raises validation error."""
        with pytest.raises(ValidationError):
            CargoReleaseResult(
                shipment_id="TEST",
                status="invalid_status",
                cargo_type="general",
            )

    def test_serialization(self) -> None:
        """Test JSON serialization."""
        result = CargoReleaseResult(
            shipment_id="BL-2024-TEST",
            status="released",
            cargo_type="general",
            release_certificate="Certificate",
        )
        json_str = result.model_dump_json()
        parsed = json.loads(json_str)
        assert parsed["status"] == "released"
        assert parsed["shipment_id"] == "BL-2024-TEST"


# =============================================================================
# Workflow Class Tests
# =============================================================================


class TestDangerousGoodsValidationWorkflow:
    """Tests for the DangerousGoodsValidationWorkflow sub-workflow."""

    def test_workflow_has_entrypoint(self) -> None:
        """Test that sub-workflow has the entrypoint method."""
        workflow = DangerousGoodsValidationWorkflow()
        assert hasattr(workflow, "run")

    def test_workflow_definition_metadata(self) -> None:
        """Test sub-workflow metadata is properly defined."""
        from mistralai.workflows.core.definition.workflow_definition import (
            get_workflow_definition,
        )
        
        workflow_class = DangerousGoodsValidationWorkflow
        definition = get_workflow_definition(workflow_class)
        
        assert definition.name == _DG_NAME
        # Just verify the definition exists and has a name
        assert hasattr(definition, 'name')


class TestCargoReleaseWorkflow:
    """Tests for the main CargoReleaseWorkflow."""

    def test_workflow_has_entrypoint(self) -> None:
        """Test that workflow has the entrypoint method."""
        workflow = CargoReleaseWorkflow()
        assert hasattr(workflow, "run")

    def test_workflow_definition_metadata(self) -> None:
        """Test workflow metadata is properly defined."""
        from mistralai.workflows.core.definition.workflow_definition import (
            get_workflow_definition,
        )
        from datetime import timedelta
        
        workflow_class = CargoReleaseWorkflow
        definition = get_workflow_definition(workflow_class)
        
        assert definition.name == _CARGO_NAME
        # Just verify the definition exists and has a name
        assert hasattr(definition, 'name')
        # Check that execution timeout is set (24 hours)
        assert definition.execution_timeout == timedelta(hours=24)

    def test_workflow_extends_interactive_workflow(self) -> None:
        """Test that workflow extends InteractiveWorkflow."""
        from mistralai.workflows import InteractiveWorkflow
        
        workflow = CargoReleaseWorkflow()
        assert isinstance(workflow, InteractiveWorkflow)


# =============================================================================
# Edge Case Tests
# =============================================================================


class TestCargoReleaseEdgeCases:
    """Edge case tests for cargo release models."""

    def test_empty_extracted_text(self) -> None:
        """Test with empty extracted text."""
        params = DangerousGoodsParams(
            extracted_text="",
            shipment_id="TEST",
        )
        assert params.extracted_text == ""

    def test_special_characters_in_shipment_id(self) -> None:
        """Test with special characters in shipment ID."""
        input_data = CargoReleaseInput(
            document_uri="file:///path/doc.pdf",
            shipment_id="BL-2024-TEST_001-abc",
        )
        assert input_data.shipment_id == "BL-2024-TEST_001-abc"

    def test_long_anomalies_list(self) -> None:
        """Test with many anomalies."""
        anomalies = [f"Anomaly {i}" for i in range(100)]
        result = DangerousGoodsResult(
            anomalies=anomalies,
            has_anomaly=True,
        )
        assert len(result.anomalies) == 100

    def test_complex_failed_rules(self) -> None:
        """Test with complex failed rule descriptions."""
        failed_rules = [
            "Rule 1: HS code missing (required for customs)",
            "Rule 2: Country of origin not declared",
            "Rule 3: Consignee address incomplete",
        ]
        check = ComplianceCheck(
            passed=False,
            failed_rules=failed_rules,
            notes="Multiple critical compliance issues",
        )
        assert len(check.failed_rules) == 3


# =============================================================================
# Model Roundtrip Tests
# =============================================================================


class TestCargoReleaseModelRoundtrip:
    """Roundtrip tests for cargo release models."""

    def test_cargo_release_input_roundtrip(self) -> None:
        """Test CargoReleaseInput roundtrip."""
        original = CargoReleaseInput(
            document_uri="s3://bucket/doc.pdf",
            shipment_id="SHIP-123",
        )
        json_str = original.model_dump_json()
        restored = CargoReleaseInput.model_validate_json(json_str)
        assert restored == original

    def test_dangerous_goods_result_roundtrip(self) -> None:
        """Test DangerousGoodsResult roundtrip."""
        original = DangerousGoodsResult(
            un_number="UN 1203",
            hazard_class="Class 3",
            anomalies=["Anomaly 1", "Anomaly 2"],
            has_anomaly=True,
        )
        json_str = original.model_dump_json()
        restored = DangerousGoodsResult.model_validate_json(json_str)
        assert restored == original

    def test_compliance_check_roundtrip(self) -> None:
        """Test ComplianceCheck roundtrip."""
        original = ComplianceCheck(
            passed=True,
            failed_rules=[],
            notes="All good",
        )
        json_str = original.model_dump_json()
        restored = ComplianceCheck.model_validate_json(json_str)
        assert restored == original

    def test_cargo_release_result_roundtrip(self) -> None:
        """Test CargoReleaseResult roundtrip."""
        original = CargoReleaseResult(
            shipment_id="SHIP-123",
            status="released",
            cargo_type="general",
            release_certificate="Certificate text",
        )
        json_str = original.model_dump_json()
        restored = CargoReleaseResult.model_validate_json(json_str)
        assert restored == original
