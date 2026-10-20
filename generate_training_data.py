"""Generate training data from real datasets."""

from src.ai_clutter_cleaner.services.dataset_loader import DatasetLoader


def main():
    """Generate training data CSV from real datasets."""
    print("Initializing dataset loader...")
    loader = DatasetLoader()

    print("\nGenerating training data from 20 Newsgroups and AG News...")
    loader.create_training_csv(
        datasets=["20newsgroups", "ag_news"],
        output_path="training_data.csv",
    )

    print("\nTraining data generated successfully!")
    print("You can now use this CSV for training the classifier.")
    print("\nTo use real data in the app:")
    print("1. Place training_data.csv in the project root")
    print("2. Set 'use_real_data=True' in the classifier initialization")
    print("3. The classifier will load from CSV instead of synthetic data")


if __name__ == "__main__":
    main()
