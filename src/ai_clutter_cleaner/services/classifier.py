"""Document classification service."""

import csv
from pathlib import Path

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline

from src.ai_clutter_cleaner.config import DEFAULT_CATEGORIES
from src.ai_clutter_cleaner.models import CategoryPrediction


class DocumentClassifier:
    """ML-based document classifier."""

    def __init__(self, use_real_data: bool = False, training_csv: str | None = None):
        """
        Initialize the classifier.

        Args:
            use_real_data: Whether to use real datasets from CSV or synthetic data
            training_csv: Path to CSV file with training data
        """
        self.pipeline = None
        self.categories = DEFAULT_CATEGORIES
        self.model_version = "1.0.0"
        self._is_trained = False
        self.use_real_data = use_real_data
        self.training_csv = training_csv

    def train(self) -> None:
        """Train the classifier with training data."""
        if self.use_real_data and self.training_csv and Path(self.training_csv).exists():
            # Load from CSV
            texts, labels = self._load_from_csv(self.training_csv)
        else:
            # Use synthetic data
            texts, labels = self._load_synthetic_data()

        if not texts:
            raise ValueError("No training data available")

        # Create and train the pipeline
        self.pipeline = make_pipeline(
            TfidfVectorizer(max_features=1000, ngram_range=(1, 2)),
            LogisticRegression(max_iter=1000, random_state=42),
        )

        self.pipeline.fit(texts, labels)
        self._is_trained = True

    def _load_synthetic_data(self) -> tuple[list[str], list[str]]:
        """Load synthetic training data."""
        # Synthetic training data for demonstration
        training_data = {
            "Work and Projects": [
                "project proposal for new software",
                "meeting minutes with team",
                "quarterly business review",
                "client presentation slides",
                "project timeline and milestones",
                "budget proposal for department",
                "contract terms and conditions",
                "work schedule and assignments",
                "team collaboration document",
                "project status report",
            ],
            "Education and Notes": [
                "lecture notes on machine learning",
                "study guide for final exam",
                "course syllabus and requirements",
                "research paper on neural networks",
                "class assignment submission",
                "textbook chapter summary",
                "lab experiment results",
                "study flashcards",
                "academic paper references",
                "course materials and readings",
            ],
            "Finance and Bills": [
                "electricity bill statement",
                "credit card statement",
                "bank account statement",
                "invoice for services",
                "tax return document",
                "receipt for purchase",
                "insurance policy document",
                "investment portfolio report",
                "loan agreement",
                "expense tracking spreadsheet",
            ],
            "Career and Resumes": [
                "curriculum vitae",
                "resume for job application",
                "cover letter template",
                "job offer letter",
                "reference letter",
                "professional certification",
                "employment contract",
                "performance review",
                "skills assessment",
                "career development plan",
            ],
            "Personal Documents": [
                "birth certificate",
                "passport application",
                "medical records",
                "personal identification",
                "wedding invitation",
                "personal journal entry",
                "family photos description",
                "personal letter",
                "address book",
                "personal budget",
            ],
            "Software and Code": [
                "python script for data analysis",
                "javascript function",
                "html and css code",
                "configuration file",
                "docker compose",
                "api documentation",
                "code review comments",
                "github repository readme",
                "software documentation",
                "debugging notes",
            ],
            "Images and Media": [
                "photo gallery description",
                "video project timeline",
                "graphic design assets",
                "audio recording notes",
                "media backup list",
                "image metadata",
                "video editing project",
                "design mockup description",
                "media library catalog",
                "render settings",
            ],
            "Miscellaneous": [
                "random notes",
                "temp file",
                "test document",
                "untitled document",
                "draft text",
                "miscellaneous information",
                "unorganized notes",
                "placeholder content",
                "sample text",
                "generic document",
            ],
        }

        texts = []
        labels = []

        for category, examples in training_data.items():
            texts.extend(examples)
            labels.extend([category] * len(examples))

        return texts, labels

    def _load_from_csv(self, csv_path: str) -> tuple[list[str], list[str]]:
        """Load training data from CSV file."""
        texts = []
        labels = []

        with open(csv_path, encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                texts.append(row["text"])
                labels.append(row["label"])

        return texts, labels

    def predict(self, text: str, filename: str = "") -> CategoryPrediction:
        """
        Predict the category of a document.

        Args:
            text: Extracted document text
            filename: Original filename (used for rule-based fallback)

        Returns:
            CategoryPrediction with category and confidence
        """
        if not self._is_trained:
            self.train()

        if not text or len(text.strip()) < 10:
            # Not enough text for ML classification
            return self._rule_based_classification(filename)

        try:
            # Get prediction and probability
            prediction = self.pipeline.predict([text])[0]
            probabilities = self.pipeline.predict_proba([text])[0]
            confidence = float(max(probabilities))

            # Get the class index
            class_idx = list(self.pipeline.classes_).index(prediction)

            source = "synthetic" if not self.use_real_data else "real-dataset"
            reason = (
                f"ML prediction based on document content "
                f"(class {class_idx}, source: {source})"
            )

            return CategoryPrediction(
                category=prediction,
                confidence=confidence,
                reason=reason,
                model_version=self.model_version,
            )
        except Exception:
            # Fallback to rule-based on error
            return self._rule_based_classification(filename)

    def _rule_based_classification(self, filename: str) -> CategoryPrediction:
        """Rule-based classification as fallback."""
        filename_lower = filename.lower()

        # Rule-based categorization based on filename patterns
        if any(
            keyword in filename_lower
            for keyword in ["resume", "cv", "cover", "application", "job"]
        ):
            return CategoryPrediction(
                category="Career and Resumes",
                confidence=0.70,
                reason="Rule-based: filename contains career-related keywords",
                model_version="rule-based-1.0.0",
            )

        if any(
            keyword in filename_lower
            for keyword in ["bill", "invoice", "receipt", "statement", "tax"]
        ):
            return CategoryPrediction(
                category="Finance and Bills",
                confidence=0.75,
                reason="Rule-based: filename contains finance-related keywords",
                model_version="rule-based-1.0.0",
            )

        if any(
            keyword in filename_lower
            for keyword in ["notes", "lecture", "study", "course", "exam"]
        ):
            return CategoryPrediction(
                category="Education and Notes",
                confidence=0.70,
                reason="Rule-based: filename contains education-related keywords",
                model_version="rule-based-1.0.0",
            )

        if any(
            keyword in filename_lower
            for keyword in ["project", "proposal", "report", "meeting", "contract"]
        ):
            return CategoryPrediction(
                category="Work and Projects",
                confidence=0.65,
                reason="Rule-based: filename contains work-related keywords",
                model_version="rule-based-1.0.0",
            )

        if any(
            keyword in filename_lower
            for keyword in [".py", ".js", ".html", ".css", ".json", "config"]
        ):
            return CategoryPrediction(
                category="Software and Code",
                confidence=0.80,
                reason="Rule-based: filename has code-related extension",
                model_version="rule-based-1.0.0",
            )

        # Default to miscellaneous
        return CategoryPrediction(
            category="Miscellaneous",
            confidence=0.50,
            reason="Rule-based: no specific keywords detected",
            model_version="rule-based-1.0.0",
        )


# Global classifier instance
_classifier_instance: DocumentClassifier | None = None


def get_classifier(
    use_real_data: bool = False, training_csv: str | None = None
) -> DocumentClassifier:
    """Get or create the global classifier instance."""
    global _classifier_instance
    if _classifier_instance is None:
        _classifier_instance = DocumentClassifier(use_real_data, training_csv)
    return _classifier_instance


def classify_document(text: str, filename: str = "") -> CategoryPrediction:
    """
    Classify a document into a category.

    Args:
        text: Extracted document text
        filename: Original filename

    Returns:
        CategoryPrediction with category and confidence
    """
    classifier = get_classifier()
    return classifier.predict(text, filename)
