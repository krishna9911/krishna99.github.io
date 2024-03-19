#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 18 20:28:21 2024

@author: krishnayadav
"""

import os
import time
from PIL import Image
from transformers import SegformerImageProcessor, AutoModelForSemanticSegmentation, SegformerForSemanticSegmentation
from urllib.parse import urlparse, urlunparse
import requests
import numpy as np
import torch.nn as nn
import torch
import matplotlib.pyplot as plt


def load_model():
    processor = SegformerImageProcessor.from_pretrained("mattmdjaga/segformer_b2_clothes")
    model = AutoModelForSemanticSegmentation.from_pretrained("mattmdjaga/segformer_b2_clothes")
    
    return processor, model

def segment_image(url, processor, model):
    class_labels = {
          0: "Background", 1: "Hat", 2: "Hair", 3: "Sunglasses", 4: "Upper-clothes", 
          5: "Skirt", 6: "Pants", 7: "Dress", 8: "Belt", 9: "Left-shoe", 10: "Right-shoe", 
          11: "Face", 12: "Left-leg", 13: "Right-leg", 14: "Left-arm", 15: "Right-arm", 
          16: "Bag", 17: "Scarf"
      }

    processor = SegformerImageProcessor.from_pretrained("mattmdjaga/segformer_b2_clothes")
    model = AutoModelForSemanticSegmentation.from_pretrained("mattmdjaga/segformer_b2_clothes")

    try:
        if url.startswith('http'):
            response = requests.get(url, stream=True)
            response.raise_for_status()  # Raise an exception for invalid HTTP response status
            image = Image.open(response.raw).convert("RGB")
        else:
            image = Image.open(url).convert("RGB")   
        
    except Exception as e:
        print(e)
    
    
    inputs = processor(images=image, return_tensors="pt")

    outputs = model(**inputs)
    logits = outputs.logits.cpu()

    upsampled_logits = nn.functional.interpolate(
        logits,
        size=image.size[::-1],
        mode="bilinear",
        align_corners=False,
    )

    pred_seg = upsampled_logits.argmax(dim=1)[0]

    included_classes = ["Face", "Hair"]

    included_class_indices = [class_idx for class_idx, class_name in class_labels.items() if class_name in included_classes]

    included_classes_mask = torch.zeros_like(pred_seg)
    for class_idx in included_class_indices:
        included_classes_mask[pred_seg == class_idx] = 1

    included_classes_mask_np = included_classes_mask.numpy().astype(np.uint8)
    
    output_image = np.array(image)
    output_image[included_classes_mask_np == 0] = 255
    
    output_image_path = "segmented_image_face.jpg"

    output_image_pil = Image.fromarray(output_image)

    if os.path.exists(output_image_path):
        os.remove(output_image_path)

    output_image_pil.save(output_image_path)
    
    return output_image_path
    
def get_segmented_image(image_path):
    processor, model = load_model()
    output_path = segment_image(image_path, processor, model)
    print(output_path)
    
    return output_path

