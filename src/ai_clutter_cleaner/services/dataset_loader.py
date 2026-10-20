"""Dataset loading and training data management."""

from collections import defaultdict
from typing import Literal

from datasets import load_dataset


class DatasetLoader:
    """Load and prepare training data from public datasets."""

    def __init__(self):
        self.category_mapping = {
            # 20 Newsgroups categories to our categories
            "alt.atheism": "Personal Documents",
            "comp.graphics": "Software and Code",
            "comp.os.ms-windows.misc": "Software and Code",
            "comp.sys.ibm.pc.hardware": "Software and Code",
            "comp.sys.mac.hardware": "Software and Code",
            "comp.windows.x": "Software and Code",
            "misc.forsale": "Personal Documents",
            "rec.autos": "Personal Documents",
            "rec.motorcycles": "Personal Documents",
            "rec.sport.baseball": "Personal Documents",
            "rec.sport.hockey": "Personal Documents",
            "sci.crypt": "Software and Code",
            "sci.electronics": "Software and Code",
            "sci.med": "Education and Notes",
            "sci.space": "Education and Notes",
            "soc.religion.christian": "Personal Documents",
            "soc.religion.misc": "Personal Documents",
            "talk.politics.misc": "Personal Documents",
            "talk.politics.guns": "Personal Documents",
            "talk.politics.mideast": "Personal Documents",
            # AG News categories
            "World": "Miscellaneous",
            "Sports": "Personal Documents",
            "Business": "Work and Projects",
            "Sci/Tech": "Software and Code",
        }

    def load_20newsgroups(self, sample_size: int = 1000) -> list[tuple[str, str]]:
        """
        Load 20 Newsgroups dataset via scikit-learn.

        Args:
            sample_size: Number of samples to load per category

        Returns:
            List of (text, category) tuples
        """
        try:
            from sklearn.datasets import fetch_20newsgroups

            data = fetch_20newsgroups(
                subset="train",
                remove=("headers", "footers", "quotes"),
                shuffle=True,
                random_state=42,
            )

            texts = data.data
            target_names = data.target_names
            targets = data.target

            # Map to our categories
            training_data = []
            category_count = defaultdict(int)

            for text, target_idx in zip(texts, targets):
                category = target_names[target_idx]
                mapped_category = self.category_mapping.get(category, "Miscellaneous")

                # Limit samples per category for better balance
                max_per_category = 100
                if category_count[mapped_category] < max_per_category:
                    training_data.append((text, mapped_category))
                    category_count[mapped_category] += 1

            return training_data

        except Exception as e:
            print(f"Error loading 20 Newsgroups: {e}")
            return []

    def load_ag_news(self, sample_size: int = 500) -> list[tuple[str, str]]:
        """
        Load AG News dataset from Hugging Face.

        Args:
            sample_size: Number of samples to load per category

        Returns:
            List of (text, category) tuples
        """
        try:
            dataset = load_dataset("fancyzhx/ag_news", split="train", streaming=True)

            training_data = []
            category_count = defaultdict(int)

            for row in dataset:
                if len(training_data) >= sample_size * 4:  # 4 categories
                    break

                text = row["text"]
                label = row["label"]
                category = dataset.features["label"].int2str(label)
                mapped_category = self.category_mapping.get(category, "Miscellaneous")

                # Limit samples per category for better balance
                max_per_category = 100
                if category_count[mapped_category] < max_per_category:
                    training_data.append((text, mapped_category))
                    category_count[mapped_category] += 1

            return training_data

        except Exception as e:
            print(f"Error loading AG News: {e}")
            return []

    def load_sts_benchmark(self, sample_size: int = 500) -> list[tuple[str, str, float]]:
        """
        Load STS Benchmark for semantic similarity evaluation.

        Args:
            sample_size: Number of sentence pairs to load

        Returns:
            List of (sentence1, sentence2, similarity_score) tuples
        """
        try:
            dataset = load_dataset("sentence-transformers/stsb", split="train", streaming=True)

            similarity_data = []

            for row in dataset:
                if len(similarity_data) >= sample_size:
                    break

                sentence1 = row["sentence1"]
                sentence2 = row["sentence2"]
                score = row["score"]

                similarity_data.append((sentence1, sentence2, score))

            return similarity_data

        except Exception as e:
            print(f"Error loading STS Benchmark: {e}")
            return []

    def load_quora_question_pairs(self, sample_size: int = 500) -> list[tuple[str, str, int]]:
        """
        Load Quora Question Pairs for duplicate detection evaluation.

        Args:
            sample_size: Number of question pairs to load

        Returns:
            List of (question1, question2, is_duplicate) tuples
        """
        try:
            dataset = load_dataset("nyu-mll/glue", "qqp", split="train", streaming=True)

            duplicate_data = []

            for row in dataset:
                if len(duplicate_data) >= sample_size:
                    break

                question1 = row["question1"]
                question2 = row["question2"]
                is_duplicate = row["label"]

                duplicate_data.append((question1, question2, is_duplicate))

            return duplicate_data

        except Exception as e:
            print(f"Error loading Quora Question Pairs: {e}")
            return []

    def create_training_csv(
        self, datasets: list[Literal["20newsgroups", "ag_news"]],
        output_path: str = "training_data.csv",
    ) -> None:
        """
        Create a unified training CSV from multiple datasets.

        Args:
            datasets: List of dataset names to include
            output_path: Path to save the CSV file
        """
        import csv

        all_data = []

        if "20newsgroups" in datasets:
            print("Loading 20 Newsgroups...")
            all_data.extend(self.load_20newsgroups(sample_size=500))

        if "ag_news" in datasets:
            print("Loading AG News...")
            all_data.extend(self.load_ag_news(sample_size=300))

        # Add more synthetic examples for underrepresented categories
        synthetic_data = [
            # Finance and Bills (add more)
            ("Quarterly expense report and budget breakdown", "Finance and Bills"),
            ("Credit card statement for October 2024", "Finance and Bills"),
            ("Electricity bill payment confirmation", "Finance and Bills"),
            ("Tax return documents and receipts", "Finance and Bills"),
            ("Bank account statement summary", "Finance and Bills"),
            ("Invoice for consulting services", "Finance and Bills"),
            ("Insurance policy renewal notice", "Finance and Bills"),
            ("Investment portfolio performance report", "Finance and Bills"),
            ("Loan application and agreement", "Finance and Bills"),
            ("Receipt for office supplies purchase", "Finance and Bills"),
            ("Budget proposal for next quarter", "Finance and Bills"),
            ("Expense tracking spreadsheet", "Finance and Bills"),
            ("Monthly subscription charges", "Finance and Bills"),
            ("Medical insurance claim form", "Finance and Bills"),
            ("Property tax assessment notice", "Finance and Bills"),
            # Career and Resumes (add more)
            ("Professional resume and CV", "Career and Resumes"),
            ("Cover letter for job application", "Career and Resumes"),
            ("Job offer letter from tech company", "Career and Resumes"),
            ("Reference letter from previous employer", "Career and Resumes"),
            ("Professional certification documents", "Career and Resumes"),
            ("Employment contract and terms", "Career and Resumes"),
            ("Performance review feedback", "Career and Resumes"),
            ("Skills assessment test results", "Career and Resumes"),
            ("Career development plan", "Career and Resumes"),
            ("LinkedIn profile summary", "Career and Resumes"),
            ("Interview preparation notes", "Career and Resumes"),
            ("Salary negotiation document", "Career and Resumes"),
            ("Professional references list", "Career and Resumes"),
            ("Work permit and visa documents", "Career and Resumes"),
            ("Promotion recommendation letter", "Career and Resumes"),
            # Images and Media (add more)
            ("Photo gallery metadata and catalog", "Images and Media"),
            ("Video project timeline and storyboard", "Images and Media"),
            ("Graphic design assets and templates", "Images and Media"),
            ("Audio recording session notes", "Images and Media"),
            ("Media backup verification list", "Images and Media"),
            ("Image editing project files", "Images and Media"),
            ("Video production schedule", "Images and Media"),
            ("Design mockup descriptions", "Images and Media"),
            ("Media library inventory", "Images and Media"),
            ("Render settings and configurations", "Images and Media"),
            ("Photography shoot planning", "Images and Media"),
            ("Podcast episode script", "Images and Media"),
            ("Animation project assets", "Images and Media"),
            ("Logo design variations", "Images and Media"),
            ("Stock footage catalog", "Images and Media"),
            # Work and Projects (add more)
            ("Meeting minutes and project timeline", "Work and Projects"),
            ("Research proposal for new initiative", "Work and Projects"),
            ("Client presentation slides deck", "Work and Projects"),
            ("Project status report and metrics", "Work and Projects"),
            ("Team collaboration document", "Work and Projects"),
            ("Budget proposal for department", "Work and Projects"),
            ("Contract terms and conditions", "Work and Projects"),
            ("Work schedule and assignments", "Work and Projects"),
            ("Project roadmap and milestones", "Work and Projects"),
            ("Business requirements document", "Work and Projects"),
            ("Stakeholder presentation", "Work and Projects"),
            ("Strategic planning notes", "Work and Projects"),
            ("Vendor proposal evaluation", "Work and Projects"),
            ("Project risk assessment", "Work and Projects"),
            ("Sprint planning document", "Work and Projects"),
            # Education and Notes (add more)
            ("Lecture notes on machine learning", "Education and Notes"),
            ("Study guide for final exam", "Education and Notes"),
            ("Course syllabus and requirements", "Education and Notes"),
            ("Research paper on neural networks", "Education and Notes"),
            ("Class assignment submission", "Education and Notes"),
            ("Textbook chapter summary", "Education and Notes"),
            ("Lab experiment results", "Education and Notes"),
            ("Study flashcards and quizzes", "Education and Notes"),
            ("Academic paper references", "Education and Notes"),
            ("Course materials and readings", "Education and Notes"),
            ("Online course completion certificate", "Education and Notes"),
            ("Research methodology notes", "Education and Notes"),
            ("Thesis proposal document", "Education and Notes"),
            ("Literature review summary", "Education and Notes"),
            ("Citation manager database", "Education and Notes"),
        ]

        all_data.extend(synthetic_data)

        # Save to CSV
        with open(output_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["text", "label", "source"])
            for text, label in all_data:
                writer.writerow([text, label, "synthetic"])

        print(f"Training data saved to {output_path} ({len(all_data)} examples)")


def load_training_data_from_csv(csv_path: str) -> list[tuple[str, str]]:
    """
    Load training data from a CSV file.

    Args:
        csv_path: Path to the CSV file

    Returns:
        List of (text, category) tuples
    """
    import csv

    training_data = []

    with open(csv_path, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            training_data.append((row["text"], row["label"]))

    return training_data
