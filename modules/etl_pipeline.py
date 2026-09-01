from modules.data_cleaning import clean_dataframe
from modules.feature_engineering import create_features
from modules.quality_engine import generate_quality_report
from modules.kpi_engine import generate_kpis

def process_dataset(df):

    cleaned_df, cleaning_report = clean_dataframe(df)

    featured_df = create_features(cleaned_df)

    quality = generate_quality_report(featured_df, cleaning_report)

    kpis = generate_kpis(featured_df)

    return {
        "data": featured_df,
        "cleaning_report": cleaning_report,
        "quality": quality,
        "kpis": kpis,
    }