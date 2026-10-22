import numpy as np
from sklearn.ensemble import IsolationForest

class ContextAwareAnomalyEngine:
    def __init__(self):
        # Operational envelope defining the designated wilderness trekking boundary
        # Configured for Sahyadri / Parsik Hill Ridge & Trails in Navi Mumbai
        self.mountain_bounds = {
            "min_lat": 18.9800, "max_lat": 19.1200,
            "min_lng": 73.0100, "max_lng": 73.1500
        }
        self.model = IsolationForest(contamination=0.03, random_state=42)
        self._train_baseline()

    def _train_baseline(self):
        """
        Train Isolation Forest on multi-modal alpine patterns:
        - 70% Active trekking (speed: 1.5 - 5.5 km/h, incline: 0 - 6 m/min)
        - 30% Viewpoint rest & hydration stops (speed: 0.0 - 0.8 km/h, pause: 2 - 20 min)
        """
        np.random.seed(42)
        normal_trekking_samples = []

        # 1. Active hiking movement patterns (350 samples)
        for _ in range(350):
            speed = np.random.normal(3.8, 0.8)
            altitude_delta = np.random.normal(2.5, 1.2)
            inactivity = np.random.exponential(2.0)
            normal_trekking_samples.append([
                max(1.0, speed),
                altitude_delta,
                min(10.0, inactivity)
            ])

        # 2. Trail rest stops, viewpoint pauses, and hydration breaks (150 samples)
        for _ in range(150):
            speed = np.random.uniform(0.0, 0.8)
            altitude_delta = np.random.normal(0.0, 0.3)
            inactivity = np.random.uniform(2.0, 20.0)  # Safe pauses up to 20 mins
            normal_trekking_samples.append([
                speed,
                altitude_delta,
                inactivity
            ])

        self.model.fit(normal_trekking_samples)

    def is_inside_mountain_domain(self, lat, lng):
        """Check if user coordinate falls within designated high-risk trail envelope."""
        return (self.mountain_bounds["min_lat"] <= lat <= self.mountain_bounds["max_lat"] and
                self.mountain_bounds["min_lng"] <= lng <= self.mountain_bounds["max_lng"])

    def evaluate_telemetry(self, lat, lng, speed, alt_rate, inactivity, gps_accuracy=10):
        """
        Context-aware hierarchical evaluation pipeline:
        1. Multipath GPS Noise Filter (Urban Signal Degradation)
        2. Spatial Context Gating (Transit Bypass vs Wilderness Trail)
        3. Isolation Forest Behavioral Scoring (Fall, Trajectory & Inactivity Anomalies)
        """
        # Step 1: Reject Urban Multipath Reflections (High Dilution of Precision)
        if gps_accuracy > 30:
            return {
                "status": "FILTERED",
                "state": "URBAN_GPS_JITTER_REJECTED",
                "score": 0.0,
                "reason": f"Signal multipath reflection detected (Accuracy: ±{gps_accuracy}m > threshold 30m). Telemetry ignored to prevent false alerts."
            }

        # Step 2: Context-Aware Spatial & Transit Gating
        # Outside designated mountain bounds OR vehicle speeds (> 20 km/h) -> Transit Mode
        if not self.is_inside_mountain_domain(lat, lng) or speed > 20.0:
            return {
                "status": "STANDBY",
                "state": "TRANSIT_MODE",
                "score": 0.0,
                "reason": f"Vehicle/Urban transit profile registered ({speed:.1f} km/h). Mountain Anomaly Detector in operational bypass."
            }

        # Step 3: Wilderness Trail Inference via Isolation Forest
        feature_vector = np.array([[speed, alt_rate, inactivity]])
        score = self.model.decision_function(feature_vector)[0]
        prediction = self.model.predict(feature_vector)[0]

        if prediction == -1:
            return {
                "status": "ALERT",
                "state": "CRITICAL_ANOMALY",
                "score": round(float(score), 4),
                "reason": "Unnatural movement signature detected inside wilderness zone (Steep drop/Fall/Prolonged trauma immobility)."
            }
        
        return {
            "status": "NORMAL",
            "state": "SAFE_TRAIL_PROGRESSION",
            "score": round(float(score), 4),
            "reason": "Standard human trekking dynamics within nominal trail safety envelope."
        }


if __name__ == "__main__":
    print("=" * 70)
    print("🧠 TourShield: Context-Aware AI Anomaly Detection Engine")
    print("   Operational Envelope: Sahyadri / Parsik Hill Ridge & Wilderness Corridor")
    print("=" * 70)

    engine = ContextAwareAnomalyEngine()
    print("✅ Isolation Forest trained on 500 calibrated trail and rest baselines.\n")

    # Real-time multi-context validation scenarios
    scenarios = [
        {
            "title": "Scenario 1: Urban Highway Commute (Navi Mumbai Palm Beach Road)",
            "lat": 19.0330, "lng": 73.0297, "speed": 45.0, "alt_rate": 0.0, "inactivity": 0.5, "acc": 12
        },
        {
            "title": "Scenario 2: Urban Skyscraper GPS Bounce (Multipath Jitter)",
            "lat": 19.0330, "lng": 73.0297, "speed": 18.0, "alt_rate": 1.0, "inactivity": 0.2, "acc": 48
        },
        {
            "title": "Scenario 3: Nominal Trail Hiking (Parsik Hill Trail)",
            "lat": 19.0410, "lng": 73.0310, "speed": 3.6, "alt_rate": 2.4, "inactivity": 2.0, "acc": 8
        },
        {
            "title": "Scenario 4: Viewpoint Rest Stop (Hydration Break)",
            "lat": 19.0420, "lng": 73.0325, "speed": 0.5, "alt_rate": 0.0, "inactivity": 8.0, "acc": 6
        },
        {
            "title": "Scenario 5: Severe Cliff Fall & Unconsciousness on Trail",
            "lat": 19.0435, "lng": 73.0340, "speed": 0.0, "alt_rate": -65.0, "inactivity": 75.0, "acc": 5
        }
    ]

    for item in scenarios:
        res = engine.evaluate_telemetry(
            item["lat"], item["lng"], item["speed"], item["alt_rate"], item["inactivity"], item["acc"]
        )
        print(f"[{item['title']}]")
        print(f"  Coordinates: ({item['lat']}, {item['lng']}) | Speed: {item['speed']} km/h | GPS Precision: ±{item['acc']}m")
        print(f"  Engine State: [{res['state']}] (Status: {res['status']})")
        if res["score"] != 0.0:
            print(f"  Anomaly Score: {res['score']}")
        print(f"  Resolution  : {res['reason']}\n{'-' * 70}")