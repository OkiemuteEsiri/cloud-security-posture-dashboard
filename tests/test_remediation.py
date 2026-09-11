import unittest
from src.remediation import validate_record


class RemediationTests(unittest.TestCase):
    def test_complete_effective_record_validates(self):
        record = {"finding_id":"F1","owner":"team","change_reference":"CHG-1","post_change_state":"secure","validation_method":"fixture check","validation_result":"effective"}
        self.assertEqual(validate_record(record).state, "validated")

    def test_missing_evidence_is_not_validated(self):
        record = {"finding_id":"F1","owner":"team","change_reference":"","post_change_state":"","validation_method":"check","validation_result":"pending"}
        decision = validate_record(record)
        self.assertEqual(decision.state, "needs_evidence")
        self.assertIn("change_reference", decision.missing_evidence)

    def test_ineffective_validation_rejects_closure(self):
        record = {"finding_id":"F1","owner":"team","change_reference":"CHG-1","post_change_state":"changed","validation_method":"check","validation_result":"ineffective"}
        self.assertEqual(validate_record(record).state, "invalid_closure")

    def test_pending_is_ready_for_validation(self):
        record = {"finding_id":"F1","owner":"team","change_reference":"CHG-1","post_change_state":"changed","validation_method":"check","validation_result":"pending"}
        self.assertEqual(validate_record(record).state, "ready_for_validation")

    def test_unknown_validation_result_rejected(self):
        record = {"finding_id":"F1","owner":"team","change_reference":"CHG-1","post_change_state":"changed","validation_method":"check","validation_result":"unknown"}
        with self.assertRaises(ValueError): validate_record(record)


if __name__ == "__main__": unittest.main()
