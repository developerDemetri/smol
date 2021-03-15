from aws_cdk.core import Construct
from aws_cdk.aws_elasticloadbalancingv2 import (
    ApplicationListener,
    ApplicationProtocol,
    ApplicationTargetGroup,
    HealthCheck,
    ListenerCondition,
    TargetType,
)
from aws_cdk.aws_elasticloadbalancingv2_targets import LambdaTarget
from aws_cdk.aws_lambda import Function


class SmolTarget(Construct):
    """
    ALB Target for Lambda
    """

    def __init__(
        self, scope: Construct, id: str, function: Function, api_host: str
    ) -> None:
        super().__init__(scope, id)
        tls_listener = ApplicationListener.from_lookup(
            self,
            "albTlsListener",
            listener_protocol=ApplicationProtocol.HTTPS,
            load_balancer_tags={"name": "ingress", "SmolIngress": "true"},
        )
        smol_target_group = ApplicationTargetGroup(
            self,
            "SmolTargetGroup",
            health_check=HealthCheck(
                enabled=True, healthy_http_codes="301", path="/mrteef"
            ),
            targets=[LambdaTarget(function)],
            target_type=TargetType.LAMBDA,
        )
        smol_api_condition = ListenerCondition.host_headers([api_host])
        tls_listener.add_target_groups(
            "SmolTarget",
            conditions=[smol_api_condition],
            priority=1,
            target_groups=[smol_target_group],
        )
