
from reports.android import android_report
from reports.blue_apple import blue_apple_report
from reports.gold_apple import gold_apple_report
from reports.orange_apple import orange_apple_report

reports_dict = {"gold_apple":gold_apple_report,
                "blue_apple":blue_apple_report,
                "gallery":android_report,
                "stripper":orange_apple_report}