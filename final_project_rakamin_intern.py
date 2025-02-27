# -*- coding: utf-8 -*-
"""Final Project Rakamin Intern

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1Kcp5mmalG22TFIxOGhi47MpPQhVeh0qa

# **Nama : I GUSTI DE AYU**

# **IMPORT DATASET**
"""

from google.colab import drive
drive.mount('/content/drive')

"""IMPORT LIBRARY"""

import pandas as pd #dataframe
import numpy as np
import seaborn as sns #visualisasi
import matplotlib.pyplot as plt #visualisasi
from sklearn.preprocessing import LabelEncoder #encoding
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

df = pd.read_csv("/content/drive/MyDrive/Colab Notebooks/06. Rakamin /loan_data_2007_2014.csv")
df.head()

"""## **EDA (Exploratory Data Analysis)**"""

df.shape

df.info()

"""melihat distribusi data"""

df.describe()

"""CEK "NaN"
"""

# Mengecek apakah ada NaN dalam DataFrame
has_nan = df.isna().any().any()
print("Apakah terdapat nilai NaN dalam data?:", has_nan)
total_nan_per_column = df.isna().sum()
columns_with_nan = total_nan_per_column[total_nan_per_column > 0]
print("Kolom dengan nilai NaN:\n", columns_with_nan)

"""CEK NILAI NOL"""

# Mengecek apakah ada NOL (0) dalam DataFrame
pd.set_option('display.max_columns', None)
pd.set_option('display.expand_frame_repr', False)
pd.set_option('display.max_rows', None)
pd.set_option('display.max_colwidth', None)
is_zero = df.applymap(lambda x: x == 0)
zero_counts_per_column = is_zero.sum()

print("Jumlah nilai nol dalam setiap kolom:\n", zero_counts_per_column)

"""DROP COLUMNS"""

import pandas as pd

# Asumsikan data Anda dalam DataFrame bernama df
cols_to_drop = [
    'Unnamed: 0',
    'id',
    'member_id',
    'emp_title',
    'url',
    'desc',
    'purpose',
    'title',
    'zip_code',
    'addr_state',
    'delinq_2yrs',
    'inq_last_6mths',
    'mths_since_last_delinq',
    'mths_since_last_record',
    'pub_rec',
    'collections_12_mths_ex_med',
    'mths_since_last_major_derog',
    'policy_code',
    'application_type',
    'annual_inc_joint',
    'dti_joint',
    'verification_status_joint',
    'acc_now_delinq',
    'tot_coll_amt',
    'tot_cur_bal',
    'out_prncp_inv',
    'out_prncp',
    'total_rec_late_fee',
    'recoveries',
    'collection_recovery_fee',
    'collections_12_mths_ex_med',
    'acc_now_delinq',
    'open_acc_6m',
    'open_il_6m',
    'open_il_12m',
    'open_il_24m',
    'mths_since_rcnt_il',
    'total_bal_il',
    'il_util',
    'open_rv_12m',
    'open_rv_24m',
    'max_bal_bc',
    'all_util',
    'total_rev_hi_lim',
    'inq_fi',
    'total_cu_tl',
    'inq_last_12m',
    'initial_list_status',
    'pymnt_plan',
    'next_pymnt_d',
    'last_pymnt_d',
    'issue_d',
    'last_credit_pull_d'
]

# Drop the columns
df.drop(columns=cols_to_drop, inplace=True)

df.info()

"""# Histogram"""

df.hist(bins=50, figsize=(10,8), color='black')

df1 = df.copy()

df1.shape

has_nan = df1.isna().any().any()
print("Apakah terdapat nilai NaN dalam data?:", has_nan)

# Jika ada NaN, hapus baris yang mengandung NaN dari salinan DataFrame
if has_nan:
    df1 = df1.dropna()
    print("Baris dengan nilai NaN telah dihapus dari df1.")

# Mengecek bentuk DataFrame setelah penghapusan
print("Bentuk DataFrame df1 setelah penghapusan baris dengan NaN:", df1.shape)

#cek baris apakah ada Nan
rows_with_nan = df1.isna().any(axis=1).sum()
print(f"Ada {rows_with_nan} baris yang mengandung nilai NaN dalam data.")

df1.isnull().sum()

# Menghitung jumlah nilai nol di setiap kolom
is_zero = df1.applymap(lambda x: x == 0)
zero_counts_per_column = is_zero.sum()
print("Jumlah nilai nol dalam setiap kolom:\n", zero_counts_per_column)

nunique_counts = df1.nunique()
print(nunique_counts)

"""# **ENCODING**

Merubah type data dari kategorikal menjadi numerical

ada 2 yang dilakukan
1. one-hot encoding untuk tipe data yang memang kategorinya bukan tingkatan.

2. LabelEncoder untuk tipe data yang kategorinya berupa tingkatan seperti grade dan sub-grade.
"""

df1.head()

# Membuat mapping urutan abjad untuk sub_grade dan grade
sub_grade_mapping = {sub_grade: idx for idx, sub_grade in enumerate(sorted(df1['sub_grade'].unique()))}
grade_mapping = {grade: idx for idx, grade in enumerate(sorted(df1['grade'].unique()))}

# Melakukan Label Encoding dengan urutan abjad
df1['sub_grade_encoded'] = df1['sub_grade'].map(sub_grade_mapping)
df1['grade_encoded'] = df1['grade'].map(grade_mapping)

# Inisialisasi LabelEncoder
label_encoder = LabelEncoder()

# Label encoding untuk kolom sub_grade dan grade
df1['sub_grade_encoded'] = label_encoder.fit_transform(df1['sub_grade'])
df1['grade_encoded'] = label_encoder.fit_transform(df1['grade'])

# Menjatuhkan kolom asli
df1.drop(columns=['sub_grade', 'grade'], inplace=True)

# Lakukan one-hot encoding pada kolom kategorikal
df1 = pd.get_dummies(df1, columns=['home_ownership', 'verification_status'], dtype=int)

#term mengambil numericnya "36 months"
df1['term_numeric'] = df1['term'].str.extract(r'(\d+)', expand=False).astype(int)
df1.drop(columns=['term'], inplace=True)

df1['emp_length'].unique()

# Fungsi untuk mengonversi emp_length ke numerik
def convert_emp_length(emp_length):
    if emp_length == '10+ years':
        return 10
    elif emp_length == '< 1 year':
        return 0
    else:
        return int(emp_length.split()[0])

# Terapkan fungsi ke kolom emp_length
df1['emp_length_numeric'] = df1['emp_length'].apply(convert_emp_length)

# Drop kolom emp_length yang asli jika tidak lagi diperlukan
df1.drop(columns=['emp_length'], inplace=True)

# Mengonversi kolom 'earliest_cr_line' menjadi format datetime
df1['earliest_cr_line'] = pd.to_datetime(df1['earliest_cr_line'], format='%b-%y')

# Mengambil tahun dari kolom 'earliest_cr_line_date'
df1['earliest_cr_line_year'] = df1['earliest_cr_line'].dt.year.astype(int)

# Drop kolom 'earliest_cr_line_date' jika tidak lagi diperlukan
df1.drop(columns=['earliest_cr_line'], inplace=True)

df1.info()

df2 = df1.copy()

df2.head()

df1['loan_status'].unique()

# Label map untuk mengklasifikasikan status pembayaran menjadi "bad" atau "good"
label_map = {
    'Fully Paid': 'good',
    'Charged Off': 'bad',
    'Current': 'good',
    'Default': 'bad',
    'Late (31-120 days)': 'bad',
    'In Grace Period': 'good',  # Dapat juga dianggap sebagai "bad" tergantung pada kebijakan pemberi pinjaman
    'Late (16-30 days)': 'bad',
    'Does not meet the credit policy. Status:Fully Paid': 'good',
    'Does not meet the credit policy. Status:Charged Off': 'bad'
}
# Menggunakan label map untuk mengonversi status pembayaran menjadi kategori "bad" atau "good"
df2['loan_status'] = df2['loan_status'].map(label_map)

df2['loan_status'] = df2['loan_status'].map({
    'bad':0,
    'good':1,
})

"""#SUDAH NUMERIC SEMUA"""

df2.head()

df2.columns

col = ['loan_amnt', 'funded_amnt', 'funded_amnt_inv', 'int_rate',
       'installment', 'annual_inc', 'loan_status', 'dti', 'open_acc',
       'revol_bal', 'revol_util', 'total_acc', 'total_pymnt',
       'total_pymnt_inv', 'total_rec_prncp', 'total_rec_int',
       'last_pymnt_amnt', 'sub_grade_encoded', 'grade_encoded',
       'home_ownership_ANY', 'home_ownership_MORTGAGE', 'home_ownership_NONE',
       'home_ownership_OTHER', 'home_ownership_OWN', 'home_ownership_RENT',
       'verification_status_Not Verified',
       'verification_status_Source Verified', 'verification_status_Verified',
       'term_numeric', 'emp_length_numeric', 'earliest_cr_line_year']

for col in df2:
    df2[col] = pd.to_numeric(df2[col], errors='coerce')

# Mengecek hasil konversi
print(df2.dtypes)

STOP

"""# Handling Outliers"""

# Plotting boxplots
plt.figure(figsize=(10, 8))

# Iterate over each column and create a horizontal boxplot
for i, column in enumerate(df2.columns):
    plt.subplot(len(df2.columns), 1, i+1)
    sns.boxplot(x=df2[column])

plt.tight_layout()
plt.show()

"""**Winsorizing data**

Winsorizing adalah teknik penting dalam pengolahan data untuk menangani outliers tanpa harus menghapus data
"""

# Winsorizing data
from scipy.stats.mstats import winsorize
numeric_features = df2.select_dtypes(include=['float64', 'int64']).columns

# Terapkan winsorizing pada setiap kolom numerik
for feature in numeric_features:
    df2[feature] = winsorize(df2[feature], limits=[0.05, 0.05])

# Plotting boxplots
plt.figure(figsize=(10, 8))

# Iterate over each column and create a horizontal boxplot
for i, column in enumerate(df2.columns):
    plt.subplot(len(df2.columns), 1, i+1)
    sns.boxplot(x=df2[column])

plt.tight_layout()
plt.show()

"""korelasi feature dengan target ['loan_status']"""

df2.corr()['loan_status']

df2['loan_status'].value_counts()

"""**SMOTE (Synthetic Minority Over-sampling Technique)**

SMOTE membuat contoh sintetis baru. Ini dilakukan dengan memilih contoh dari kelas minoritas dan kemudian membuat contoh baru yang terletak di antara contoh tersebut dan tetangga terdekatnya. Contoh sintetis dibuat dengan interpolasi antara titik data kelas minoritas yang ada.
"""

sns.countplot(x='loan_status', data = df2)

df3 = df2.copy()

x = df3.drop(columns=['loan_status'])
y = df3['loan_status']

from imblearn.over_sampling import SMOTE
sm = SMOTE()
x_res, y_res = sm.fit_resample(x, y)

sns.countplot(x=y_res)

"""# MODELING"""

x_train, x_test, y_train, y_test = train_test_split(x_res, y_res, test_size=0.15, stratify=y_res)

#normalisasi
scaler = StandardScaler()
x_train_scaled = scaler.fit_transform(x_train)
x_test_scaled = scaler.transform(x_test)

import pandas as pd #dataframe
import seaborn as sns #visualisasi
import matplotlib.pyplot as plt #visualisasi
from sklearn.preprocessing import MinMaxScaler, StandardScaler, RobustScaler
from sklearn.preprocessing import LabelEncoder #encoding
from scipy import stats
from sklearn.impute import KNNImputer #imputasi
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import mean_squared_error
from sklearn.metrics import accuracy_score

dtree = DecisionTreeClassifier(random_state=0)
rfc = RandomForestClassifier(random_state=2)
lr = LogisticRegression(random_state=42)
knn = KNeighborsClassifier(n_neighbors=3)
abc = AdaBoostClassifier(n_estimators=50,learning_rate=1, random_state=0)
gnb = GaussianNB()

dtree.fit(x_train,y_train)
rfc.fit(x_train,y_train)
lr.fit(x_train,y_train)
knn.fit(x_train,y_train)
abc.fit(x_train, y_train)
gnb.fit(x_train, y_train)

from sklearn.metrics import accuracy_score

# Membuat prediksi untuk setiap model
y_pred_dtree = dtree.predict(x_test)
y_pred_rfc = rfc.predict(x_test)
y_pred_lr = lr.predict(x_test)
y_pred_knn = knn.predict(x_test)
y_pred_abc = abc.predict(x_test)
y_pred_gnb = gnb.predict(x_test)

# Menghitung akurasi untuk setiap model
accuracy_dtree = accuracy_score(y_test, y_pred_dtree)
accuracy_rfc = accuracy_score(y_test, y_pred_rfc)
accuracy_lr = accuracy_score(y_test, y_pred_lr)
accuracy_knn = accuracy_score(y_test, y_pred_knn)
accuracy_abc = accuracy_score(y_test, y_pred_abc)
accuracy_gnb = accuracy_score(y_test, y_pred_gnb)

# Menampilkan akurasi
print("Decision Tree Classifier Accuracy:", accuracy_dtree)
print("Random Forest Classifier Accuracy:", accuracy_rfc)
print("Logistic Regression Accuracy:", accuracy_lr)
print("K-Nearest Neighbors Classifier Accuracy:", accuracy_knn)
print("AdaBoost Classifier Accuracy:", accuracy_abc)
print("Gaussian Naive Bayes Accuracy:", accuracy_gnb)

"""1. Random Forest Classifier menunjukkan kinerja terbaik dengan akurasi 0.9724. Ini diharapkan karena Random Forest menggabungkan banyak pohon keputusan dan secara efektif mengurangi overfitting serta menangani variabilitas dalam data.

2. Decision Tree Classifier juga menunjukkan kinerja yang baik dengan akurasi 0.9445, namun mungkin lebih rentan terhadap overfitting dibandingkan Random Forest.

3. Logistic Regression memiliki akurasi yang lebih rendah, yang mungkin menunjukkan bahwa hubungan dalam data tidak sepenuhnya linier.

4. KNN dan AdaBoost menunjukkan kinerja yang cukup baik, masing-masing dengan akurasi 0.9197 dan 0.9116. Ini menunjukkan bahwa kedua metode tersebut juga mampu menangkap pola dalam data dengan cukup baik.

5. Gaussian Naive Bayes memiliki kinerja terendah, yang mungkin disebabkan oleh asumsi independensi yang kuat antar fitur.
"""

from sklearn.metrics import accuracy_score, precision_score, recall_score, roc_auc_score, confusion_matrix, classification_report
# Evaluate Decision Tree Classifier
print("Decision Tree Classifier")
print("Accuracy:", accuracy_score(y_test, y_pred_dtree))
print("Precision:", precision_score(y_test, y_pred_dtree))
print("Recall:", recall_score(y_test, y_pred_dtree))
print("ROC-AUC:", roc_auc_score(y_test, y_pred_dtree))
print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred_dtree))
print("Classification Report:\n", classification_report(y_test, y_pred_dtree))

# Evaluate Random Forest Classifier
print("\nRandom Forest Classifier")
print("Accuracy:", accuracy_score(y_test, y_pred_rfc))
print("Precision:", precision_score(y_test, y_pred_rfc))
print("Recall:", recall_score(y_test, y_pred_rfc))
print("ROC-AUC:", roc_auc_score(y_test, y_pred_rfc))
print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred_rfc))
print("Classification Report:\n", classification_report(y_test, y_pred_rfc))

# Evaluate Logistic Regression
print("\nLogistic Regression")
print("Accuracy:", accuracy_score(y_test, y_pred_lr))
print("Precision:", precision_score(y_test, y_pred_lr))
print("Recall:", recall_score(y_test, y_pred_lr))
print("ROC-AUC:", roc_auc_score(y_test, y_pred_lr))
print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred_lr))
print("Classification Report:\n", classification_report(y_test, y_pred_lr))

# Evaluate K-Nearest Neighbors Classifier
print("\nK-Nearest Neighbors Classifier")
print("Accuracy:", accuracy_score(y_test, y_pred_knn))
print("Precision:", precision_score(y_test, y_pred_knn))
print("Recall:", recall_score(y_test, y_pred_knn))
print("ROC-AUC:", roc_auc_score(y_test, y_pred_knn))
print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred_knn))
print("Classification Report:\n", classification_report(y_test, y_pred_knn))

# Evaluate AdaBoost Classifier
print("\nAdaBoost Classifier")
print("Accuracy:", accuracy_score(y_test, y_pred_abc))
print("Precision:", precision_score(y_test, y_pred_abc))
print("Recall:", recall_score(y_test, y_pred_abc))
print("ROC-AUC:", roc_auc_score(y_test, y_pred_abc))
print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred_abc))
print("Classification Report:\n", classification_report(y_test, y_pred_abc))

# Evaluate Gaussian Naive Bayes
print("\nGaussian Naive Bayes")
print("Accuracy:", accuracy_score(y_test, y_pred_gnb))
print("Precision:", precision_score(y_test, y_pred_gnb))
print("Recall:", recall_score(y_test, y_pred_gnb))
print("ROC-AUC:", roc_auc_score(y_test, y_pred_gnb))
print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred_gnb))
print("Classification Report:\n", classification_report(y_test, y_pred_gnb))

import pandas as pd
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import KFold

# Inisialisasi K-Fold Cross-Validation
kf = KFold(n_splits=5, shuffle=True, random_state=42)

# Cross-Validation untuk Random Forest Classifier
cv_scores_rfc = cross_val_score(rfc, x, y, cv=kf, scoring='accuracy')

# Cross-Validation untuk Logistic Regression
cv_scores_lr = cross_val_score(lr, x, y, cv=kf, scoring='accuracy')

# Cetak hasil
print("Random Forest Classifier Cross-Validation Accuracy: ", cv_scores_rfc)
print("Mean Accuracy: ", cv_scores_rfc.mean())
print("Logistic Regression Cross-Validation Accuracy: ", cv_scores_lr)
print("Mean Accuracy: ", cv_scores_lr.mean())

# Fungsi untuk menampilkan Confusion Matrix
def plot_confusion_matrix(y_test, y_pred, title):
    cm = confusion_matrix(y_test, y_pred)
    df_cm = pd.DataFrame(cm, index=['Class 0', 'Class 1'], columns=['Class 0', 'Class 1'])
    plt.figure(figsize=(8, 6))
    sns.heatmap(df_cm, annot=True, fmt='d', cmap='Blues', cbar=False)
    plt.xlabel('Predicted Labels')
    plt.ylabel('True Labels')
    plt.title(title)
    plt.show()


plot_confusion_matrix(y_test, y_pred_rfc, "Random Forest Classifier Confusion Matrix")

plot_confusion_matrix(y_test, y_pred_lr, "Logistic Regression Confusion Matrix")