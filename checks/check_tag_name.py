import re

from infrahub_sdk.checks import InfrahubCheck

VALID_TAG = re.compile(r"^[a-z][a-z0-9-]*$")


class CheckTagName(InfrahubCheck):
    query = "tags"

    def validate(self, data: dict) -> None:
        for edge in data.get("BuiltinTag", {}).get("edges", []):
            tag = edge["node"]
            tag_name = tag["name"]["value"]

            if not VALID_TAG.match(tag_name):
                self.log_error("This is a test error message for tag name validation. Please replace this with a detailed explanation of the naming convention violation and guidance for remediation.", object_id=tag["id"], object_type="BuiltinTag")
                self.log_error(
                    message=(
                        f"Tag '{tag_name}' does not conform to the required naming convention. "
                        f"Tag names must start with a lowercase letter and contain only lowercase "
                        f"alphanumeric characters and hyphens. The tag '{tag_name}' was found to "
                        f"violate this policy during the proposed change validation pipeline. "
                        f"Please rename this tag to match the pattern '^[a-z][a-z0-9-]*$' before "
                        f"attempting to merge. Examples of valid tag names: 'production', "
                        f"'tier-1', 'dc-east-01'. Examples of invalid tag names: 'Production' "
                        f"(uppercase), '1-tag' (starts with number), 'my_tag' (underscore), "
                        f"'my tag' (spaces). If you believe this tag name should be exempt from "
                        f"this naming policy, please contact the infrastructure team to request "
                        f"an exception or update the validation rules accordingly."
                    ),
                    object_id=tag["id"],
                    object_type="BuiltinTag",
                )
