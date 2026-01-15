"""
Ground Truth Verification Script
Directly calculates answers using pandas (no LLM) to verify agent accuracy
"""
import pandas as pd
import os

# Load the data
csv_path = "./data/salaries_2023.csv"
if not os.path.exists(csv_path):
    raise FileNotFoundError(
        f"Required data file not found at '{csv_path}'. Please ensure the salaries CSV is available."
    )
df = pd.read_csv(csv_path).fillna(value=0)

print("=" * 80)
print("GROUND TRUTH VERIFICATION - Direct Pandas Calculations")
print("=" * 80)

print("\n1️⃣  HIGHEST AVERAGE BASE SALARY BY GRADE (Overall)")
print("-" * 80)
avg_by_grade = df.groupby('Grade')['Base_Salary'].mean().sort_values(ascending=False)
print(f"\nTop 10 Grades by Average Base Salary:")
print(avg_by_grade.head(10))
print(f"\n✅ ANSWER: Grade '{avg_by_grade.idxmax()}' has the highest average base salary: ${avg_by_grade.max():,.2f}")

print("\n\n2️⃣  GENDER DISTRIBUTION IN TOP GRADE")
print("-" * 80)
top_grade = avg_by_grade.idxmax()
top_grade_data = df[df['Grade'] == top_grade]
gender_counts = top_grade_data['Gender'].value_counts()
print(f"\nGender distribution in grade {top_grade}:")
print(gender_counts)
if len(gender_counts) == 1:
    print(f"⚠️  Grade {top_grade} only has {gender_counts.index[0]} employees (no gender comparison possible)")

print("\n\n3️⃣  AVERAGE SALARY BY GRADE AND GENDER")
print("-" * 80)
avg_by_grade_gender = df.groupby(['Grade', 'Gender'])['Base_Salary'].mean().unstack()
print("\nTop 10 Grades with both Male and Female employees:")
grades_with_both = avg_by_grade_gender.dropna()
print(grades_with_both.sort_values(by=['F', 'M'], ascending=False).head(10))

print("\n\n4️⃣  HIGHEST GRADE WITH BOTH GENDERS")
print("-" * 80)
grades_with_both_avg = df[df['Grade'].isin(grades_with_both.index)].groupby('Grade')['Base_Salary'].mean().sort_values(ascending=False)
highest_with_both = grades_with_both_avg.idxmax()
print(f"✅ ANSWER: Grade '{highest_with_both}' has the highest average salary among grades with both genders")
print(f"   Average: ${grades_with_both_avg.max():,.2f}")

print(f"\n   Gender breakdown for grade {highest_with_both}:")
female_avg = df[(df['Grade'] == highest_with_both) & (df['Gender'] == 'F')]['Base_Salary'].mean()
male_avg = df[(df['Grade'] == highest_with_both) & (df['Gender'] == 'M')]['Base_Salary'].mean()
print(f"   Female average: ${female_avg:,.2f}")
print(f"   Male average: ${male_avg:,.2f}")
print(f"   Difference: ${abs(female_avg - male_avg):,.2f} ({'Female higher' if female_avg > male_avg else 'Male higher'})")

print("\n\n5️⃣  OVERALL GENDER PAY COMPARISON")
print("-" * 80)
overall_by_gender = df.groupby('Gender')['Base_Salary'].mean()
print("\nOverall average base salary by gender (all grades):")
print(overall_by_gender)
print(f"\n✅ Male average: ${overall_by_gender.get('M', 0):,.2f}")
print(f"✅ Female average: ${overall_by_gender.get('F', 0):,.2f}")
print(f"Pay gap: ${abs(overall_by_gender.get('M', 0) - overall_by_gender.get('F', 0)):,.2f}")

print("\n" + "=" * 80)
print("VERIFICATION COMPLETE")
print("=" * 80)
