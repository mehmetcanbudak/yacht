from typing import Union

from stable_baselines3 import PPO
from stable_baselines3.common.base_class import BaseAlgorithm
from torch import nn

from yacht.agents.modules.day import MultipleTimeFramesFeatureExtractor, DayForecastNetwork
from yacht.agents.policies.generic import GenericActorCriticPolicy
from yacht.config.proto.net_architecture_pb2 import NetArchitectureConfig
from yacht.environments import TradingEnv

agents_registry = {
    'PPO': PPO
}

policy_registry = {
    'MlpPolicy': 'MlpPolicy'
}

feature_extractor_registry = {
    'MultipleTimeFramesFeatureExtractor': MultipleTimeFramesFeatureExtractor
}

activation_fn_registry = {
    'ReLU': nn.ReLU
}


def build_agent(config, env: TradingEnv, resume: bool = False, agent_path: str = None) -> BaseAlgorithm:
    agent_config = config.agent
    policy_config = config.agent.policy
    feature_extractor_config = policy_config.feature_extractor
    input_config = config.input
    train_config = config.train

    # The agent is the main wrapper over all the logic.
    agent_class = agents_registry[agent_config.name]
    if resume:
        assert agent_path is not None

        return agent_class.load(agent_path)
    else:
        # The agent has a policy.
        policy_class = policy_registry[policy_config.name]
        # The policy will build the feature_extractor.
        feature_extractor_class = feature_extractor_registry[policy_config.feature_extractor.name]
        activation_fn_class = activation_fn_registry[policy_config.activation_fn]
        policy_kwargs = {
            'net_arch': _build_net_arch_dict(policy_config.net_arch),
            'activation_fn': activation_fn_class,
            'features_extractor_class': feature_extractor_class,
            'features_extractor_kwargs': {
                'features_dim': feature_extractor_config.output_features_dim,
                'activation_fn': activation_fn_class,
                'intervals': input_config.intervals,
                'features': input_config.features
            }
        }

        # TODO: Look over all Agents hyper-parameters
        return agent_class(
            policy=policy_class,
            env=env,
            verbose=agent_config.verbose,
            learning_rate=train_config.learning_rate,
            n_steps=train_config.collecting_n_steps,
            batch_size=train_config.batch_size,
            n_epochs=train_config.n_epochs,
            policy_kwargs=policy_kwargs
        )


def _build_net_arch_dict(net_arch: NetArchitectureConfig) -> Union[list, dict]:
    is_policy_based = len(net_arch.shared) > 0 and len(net_arch.vf) > 0
    structured_net_arch = [] if is_policy_based else dict()

    if is_policy_based:
        structured_net_arch.extend(net_arch.shared)
        structured_net_arch.append({
            'vf': list(net_arch.vf),
            'pi': list(net_arch.pi)
        })
    else:
        structured_net_arch['qf'] = list(net_arch.qf)
        structured_net_arch['pi'] = list(net_arch.pi)

    return structured_net_arch


