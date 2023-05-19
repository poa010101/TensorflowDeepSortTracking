from __future__ import division, print_function, absolute_import

import argparse
import os

import cv2
import numpy as np

from ObjectTracking.application_util import preprocessing
from ObjectTracking.deep_sort import nn_matching
from ObjectTracking.deep_sort.detection import Detection
from ObjectTracking.deep_sort.tracker import Tracker

class DeepSortTracker():
    def __init__(self, min_confidence=0.8, nms_max_overlap=1.0, min_detection_height=0.0,
                 nn_budget=None, max_cosine_distance=0.2, max_age=3):
        """
        Parameters
        ----------
        min_confidence : float
            Detection confidence threshold. Disregard all detections that have
            a confidence lower than this value.
        nms_max_overlap : float
            Maximum detection overlap (non-maxima suppression threshold).
        min_detection_height : int
            Detection height threshold. Disregard all detections that have
            a height lower than this value.
        max_cosine_distance : float
            Gating threshold for cosine distance metric (object appearance).
        nn_budget : Optional[int]
            Maximum size of the appearance descriptor gallery. If None, no budget
            is enforced.
        max_age : int
            Maximum number of missed misses before a track is deleted.
        """

        self.min_confidence = min_confidence
        self.nms_max_overlap = nms_max_overlap
        self.min_detection_height = min_detection_height
        self.max_cosine_distance = max_cosine_distance
        self.nn_budget = nn_budget

        self.metric = nn_matching.NearestNeighborDistanceMetric(
            "cosine", self.max_cosine_distance, self.nn_budget)
        self.tracker = Tracker(self.metric, max_age)

    def resetTracker(self):
        '''
        Resets the tracker
        '''
        self.tracker = Tracker(self.metric)

    def run(self, output_data, image_np):
        """Run multi-target tracker on one time step."""
        height, width, _ = image_np.shape

        # Load the detections
        detections = []
        for box, score in zip(output_data.bbs, output_data.scores):
            detections.append(Detection(box, score, image_np))

        # Load image and generate detections.
        detections = [d for d in detections if d.confidence >= self.min_confidence]

        # Run non-maxima suppression.
        boxes = np.array([d.tlwh for d in detections])
        scores = np.array([d.confidence for d in detections])
        indices = preprocessing.non_max_suppression(boxes, self.nms_max_overlap, scores)
        detections = [detections[i] for i in indices]

        # Update tracker.
        self.tracker.predict()
        self.tracker.update(detections)

        # Collect tracking results
        tracked_bbs = []
        tracker_ids = []
        for track in self.tracker.tracks:
            if track.is_confirmed() and track.time_since_update <= 1:
                bbox = track.to_tlbr_norm(width, height)
                track_id = track.track_id
                tracked_bbs.append(bbox)
                tracker_ids.append(track_id)

        # Convert the results to numpy arrays
        tracked_bbs = np.array(tracked_bbs)
        tracker_ids = np.array(tracker_ids)

        # Update the output data
        output_data.tracked_bbs = tracked_bbs
        output_data.tracker_ids = tracker_ids

        return output_data

