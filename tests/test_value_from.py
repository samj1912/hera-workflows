import pytest
from argo_workflows.models import (
    ConfigMapKeySelector,
    IoArgoprojWorkflowV1alpha1ValueFrom,
)

from hera.value_from import ValueFrom


class TestValueFrom:
    def test_raises_on_all_none_fields(self):
        with pytest.raises(ValueError) as e:
            ValueFrom()
        assert str(e.value) == "At least one fields must be not `None` for `ValueFrom`"

    def test_builds_as_expected(self):
        vf_ = ValueFrom(config_map_key_ref="abc")
        vf = vf_.build()
        assert isinstance(vf, IoArgoprojWorkflowV1alpha1ValueFrom)
        assert hasattr(vf, "config_map_key_ref")
        assert isinstance(vf.config_map_key_ref, ConfigMapKeySelector)
        assert hasattr(vf.config_map_key_ref, "key")
        assert vf.config_map_key_ref.key == "abc"
        assert not hasattr(vf, "default")
        assert not hasattr(vf, "event")
        assert not hasattr(vf, "expression")
        assert not hasattr(vf, "jq_filter")
        assert not hasattr(vf, "json_path")
        assert not hasattr(vf, "parameter")
        assert not hasattr(vf, "path")

        fields_to_test = ["default", "event", "expression", "jq_filter", "json_path", "parameter", "path"]
        # ensure this captures added fields in the future
        assert set(list(vars(vf_).keys())) == set(fields_to_test + ["config_map_key_ref"])

        for field_to_test in fields_to_test:
            vf = ValueFrom(**{field_to_test: "abc"}).build()
            assert isinstance(vf, IoArgoprojWorkflowV1alpha1ValueFrom)
            assert not hasattr(vf, "config_map_key_ref")
            assert hasattr(vf, field_to_test)
            assert vf.get(field_to_test) == "abc"
            for other_field in fields_to_test:
                if other_field == field_to_test:
                    continue
                assert not hasattr(vf, other_field)
