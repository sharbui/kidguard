"""Face recognition module.

Identifies family members or estimates age of unknown viewers.
"""

import asyncio
from pathlib import Path
from loguru import logger

try:
    import cv2
except ImportError:
    cv2 = None

try:
    import face_recognition
except ImportError:
    face_recognition = None


class FaceRecognizer:
    """Recognizes family members and estimates ages."""
    
    def __init__(self, family_config: list):
        self.family = family_config
        self.known_encodings = {}
        self.camera = None
        
        # Load known face encodings
        self._load_encodings()
        logger.info(f"FaceRecognizer initialized with {len(self.family)} family members")
    
    def _load_encodings(self):
        """Load saved face encodings for family members."""
        encodings_dir = Path("encodings")
        
        for member in self.family:
            name = member.get("name")
            encoding_file = encodings_dir / f"{name}.pkl"
            
            if encoding_file.exists():
                import pickle
                with open(encoding_file, "rb") as f:
                    self.known_encodings[name] = pickle.load(f)
                logger.debug(f"Loaded encoding for {name}")
    
    async def identify_viewer(self) -> dict | None:
        """Capture webcam image and identify the viewer.
        
        Returns:
            dict with viewer info or None if no face detected
        """
        if cv2 is None:
            logger.warning("OpenCV not installed")
            return None
        
        # Capture frame from webcam
        frame = await self._capture_webcam()
        if frame is None:
            return None
        
        # Try to identify known family member
        viewer = await self._identify_face(frame)
        
        if viewer:
            return viewer
        
        # Unknown face - estimate age
        age = await self._estimate_age(frame)
        if age is not None:
            return {
                "name": "Unknown",
                "age": age,
                "is_child": age < 12,
                "confidence": 0.6
            }
        
        return None
    
    async def _capture_webcam(self):
        """Capture a frame from the webcam."""
        if cv2 is None:
            return None
        
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            logger.warning("Could not open webcam")
            return None
        
        ret, frame = cap.read()
        cap.release()
        
        if not ret:
            logger.warning("Could not read from webcam")
            return None
        
        return frame
    
    async def _identify_face(self, frame) -> dict | None:
        """Try to identify a known family member."""
        if face_recognition is None:
            logger.warning("face_recognition not installed")
            return None
        
        # Convert BGR to RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Find faces
        face_locations = face_recognition.face_locations(rgb_frame)
        if not face_locations:
            logger.debug("No faces detected")
            return None
        
        # Get encodings
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
        
        for encoding in face_encodings:
            # Compare with known faces
            for name, known_encoding in self.known_encodings.items():
                matches = face_recognition.compare_faces([known_encoding], encoding)
                if matches[0]:
                    # Found a match
                    member = next((m for m in self.family if m["name"] == name), None)
                    if member:
                        return {
                            "name": member["name"],
                            "age": member.get("age", 0),
                            "is_child": member.get("is_child", False),
                            "confidence": 0.9
                        }
        
        return None
    
    async def _estimate_age(self, frame) -> int | None:
        """Estimate age using Claude Vision or DeepFace.
        
        TODO: Implement age estimation
        - Option 1: Use Claude Vision API
        - Option 2: Use DeepFace library
        """
        # Placeholder - return None for now
        logger.debug("Age estimation not yet implemented")
        return None
    
    async def register_face(self, name: str, age: int, is_child: bool = True):
        """Register a new family member's face.
        
        Captures webcam and saves the face encoding.
        """
        if face_recognition is None:
            logger.error("face_recognition not installed")
            return False
        
        frame = await self._capture_webcam()
        if frame is None:
            return False
        
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        face_locations = face_recognition.face_locations(rgb_frame)
        if not face_locations:
            logger.error("No face detected for registration")
            return False
        
        encoding = face_recognition.face_encodings(rgb_frame, face_locations)[0]
        
        # Save encoding
        encodings_dir = Path("encodings")
        encodings_dir.mkdir(exist_ok=True)
        
        import pickle
        with open(encodings_dir / f"{name}.pkl", "wb") as f:
            pickle.dump(encoding, f)
        
        self.known_encodings[name] = encoding
        logger.info(f"Registered face for {name}")
        return True
