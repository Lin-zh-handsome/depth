"""ManiSkill replayed RGB-D trajectories exposed through the official DP Dataset API."""
from __future__ import annotations

import copy
import numpy as np
import torch

from diffusion_policy.dataset.base_dataset import BaseImageDataset
from diffusion_policy.common.replay_buffer import ReplayBuffer
from diffusion_policy.common.sampler import SequenceSampler, get_val_mask
from diffusion_policy.model.common.normalizer import LinearNormalizer, SingleFieldLinearNormalizer
from diffusion_policy.common.normalize_util import get_image_range_normalizer


class ManiSkillRGBDImageDataset(BaseImageDataset):
    def __init__(self, zarr_path: str, horizon: int = 16, pad_before: int = 1,
                 pad_after: int = 7, n_obs_steps: int = 2, seed: int = 42,
                 val_ratio: float = 0.02):
        super().__init__()
        self.replay_buffer = ReplayBuffer.create_from_path(zarr_path, mode="r")
        self.horizon, self.pad_before, self.pad_after = horizon, pad_before, pad_after
        self.n_obs_steps = n_obs_steps
        val_mask = get_val_mask(self.replay_buffer.n_episodes, val_ratio, seed)
        self.train_mask = ~val_mask
        self.obs_keys = ("base_camera_image", "base_camera_depth",
                         "hand_camera_image", "hand_camera_depth", "agent_pos")
        self.sampler = SequenceSampler(
            replay_buffer=self.replay_buffer, sequence_length=horizon,
            pad_before=pad_before, pad_after=pad_after,
            episode_mask=self.train_mask,
            key_first_k={key: n_obs_steps for key in self.obs_keys})

    def get_validation_dataset(self):
        result = copy.copy(self)
        result.sampler = SequenceSampler(
            replay_buffer=self.replay_buffer, sequence_length=self.horizon,
            pad_before=self.pad_before, pad_after=self.pad_after,
            episode_mask=~self.train_mask,
            key_first_k={key: self.n_obs_steps for key in self.obs_keys})
        return result

    def get_normalizer(self, **kwargs):
        normalizer = LinearNormalizer()
        normalizer.fit({"action": self.replay_buffer["action"][:],
                        "agent_pos": self.replay_buffer["agent_pos"][:]},
                       last_n_dims=1, mode="limits", **kwargs)
        for key in ("base_camera_image", "hand_camera_image"):
            normalizer[key] = get_image_range_normalizer()
        for key in ("base_camera_depth", "hand_camera_depth"):
            normalizer[key] = SingleFieldLinearNormalizer.create_identity()
        return normalizer

    def __len__(self):
        return len(self.sampler)

    def __getitem__(self, idx):
        sample = self.sampler.sample_sequence(idx)
        obs = {}
        for key in self.obs_keys:
            arr = sample[key][:self.n_obs_steps]
            if key.endswith("_image"):
                arr = np.moveaxis(arr, -1, 1).astype(np.float32) / 255.0
            elif key.endswith("_depth"):
                arr = np.moveaxis(arr, -1, 1).astype(np.float32)
            else:
                arr = arr.astype(np.float32)
            obs[key] = torch.from_numpy(np.ascontiguousarray(arr))
        return {"obs": obs, "action": torch.from_numpy(sample["action"].astype(np.float32))}
