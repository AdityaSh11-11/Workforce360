from modules.workforce_cleaning import clean_workforce_data
from modules.workforce_features import create_workforce_features
from modules.workforce_quality import calculate_quality_score
from modules.workforce_kpis import workforce_kpis


def process_workforce_dataset(df):

    cleaned_df, report = clean_workforce_data(df)

    feature_df = create_workforce_features(cleaned_df)

    quality = calculate_quality_score(feature_df, report)

    kpis = workforce_kpis(feature_df)

    return {
        "data": feature_df,
        "quality": quality,
        "report": report,
        "kpis": kpis,
    }