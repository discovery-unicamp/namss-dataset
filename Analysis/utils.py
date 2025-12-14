from torch import Tensor, nn
import gc
import numpy as np
import torch
import torch.nn.functional as F
import torchvision.models.segmentation as models

class ResNetLike(nn.Module):
    def __init__(self, model):
        super().__init__()
        self.model = model
    
    def forward(self, x: Tensor) -> Tensor:
        x = self.model.backbone(x)["out"]
        x = torch.nn.functional.avg_pool2d(x, kernel_size=x.shape[2:])  # These should be removed for deeplabv3
        x = torch.flatten(x, 1)
        return x


def model_resnet50_coco():
    model = models.deeplabv3_resnet50(weights="COCO_WITH_VOC_LABELS_V1")
    model.classifier = nn.Identity()
    return ResNetLike(model)
    

def model_dinov2_vitb14():
    model = torch.hub.load('facebookresearch/dinov2', 'dinov2_vitb14')
    model.head = nn.Identity()
    return model

def model_dinov2_vitl14():
    model = torch.hub.load('facebookresearch/dinov2', 'dinov2_vitl14')
    model.head = nn.Identity()
    return model

def model_dinov2_vitg14():
    model = torch.hub.load('facebookresearch/dinov2', 'dinov2_vitg14')
    model.head = nn.Identity()
    return model


def pad_to_multiple(img, patch_size):
    """
    Pads an image (C,H,W) so that H and W become the nearest *higher*
    multiple of patch_size. Padding is symmetric (image stays centered).
    """
    C, H, W = img.shape

    # compute target sizes
    new_H = ((H + patch_size - 1) // patch_size) * patch_size
    new_W = ((W + patch_size - 1) // patch_size) * patch_size

    # padding amounts
    pad_H = new_H - H
    pad_W = new_W - W

    pad_top    = pad_H // 2
    pad_bottom = pad_H - pad_top
    pad_left   = pad_W // 2
    pad_right  = pad_W - pad_left

    # pad: (left, right, top, bottom)
    return F.pad(img, (pad_left, pad_right, pad_top, pad_bottom), mode="constant", value=0)


def free_gc_decorator(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        torch.cuda.empty_cache()
        import gc
        gc.collect()
        return result
    return wrapper


