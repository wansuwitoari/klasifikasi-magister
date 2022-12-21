import streamlit as st
from numpy import mean
from numpy import std
import os
import pandas as pd
import numpy as np
from pandas import DataFrame
import plotly.express as px

from sklearn.ensemble import RandomForestClassifier

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from imblearn.over_sampling import SMOTE, ADASYN, BorderlineSMOTE


from pyxlsb import open_workbook as open_xlsb
from io import BytesIO


def to_excel(df):
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, index=False, sheet_name='Sheet1')
    workbook = writer.book
    worksheet = writer.sheets['Sheet1']
    format1 = workbook.add_format({'num_format': '0.00'})
    worksheet.set_column('A:A', None, format1)
    writer.save()
    processed_data = output.getvalue()
    return processed_data


data = pd.read_csv('fix4.csv')
X = data.drop('Lama_Kuliah', axis=1)
y = data['Lama_Kuliah']

# build the scaler model
X = pd.DataFrame(MinMaxScaler().fit_transform(X),
                 columns=X.columns, index=X.index)
X_resampled, y_resampled = SMOTE().fit_resample(X, y)
X_resampled = X_resampled.drop(
    ['Jenis_Beasiswa'], axis=1)

X_train, X_test, y_train, y_test = train_test_split(
    X_resampled, y_resampled, test_size=0.2)
# fit the model
model = RandomForestClassifier(bootstrap=True,
                               max_depth=None,
                               max_features=2,
                               min_samples_leaf=2,
                               min_samples_split=5,
                               n_estimators=162)
model.fit(X_train, y_train)

# build the scaler model
X2 = data.drop('Lama_Kuliah', axis=1)
X2 = pd.DataFrame(MinMaxScaler().fit_transform(X2),
                  columns=X2.columns, index=X2.index)
X2_resampled, y_resampled = SMOTE().fit_resample(X2, y)
X2_resampled = X2_resampled.drop(
    ['Motivasi_Studi', 'Jenis_TPA', 'Jenis_Beasiswa'], axis=1)

X2_train, X2_test, y_train, y_test = train_test_split(
    X2_resampled, y_resampled, test_size=0.2)
# fit the model
model2 = RandomForestClassifier(bootstrap=True,
                                max_depth=None,
                                max_features=2,
                                min_samples_leaf=2,
                                min_samples_split=5,
                                n_estimators=162)
model2.fit(X2_train, y_train)


st.sidebar.image("logo_magister.png", use_column_width=True)
option = st.sidebar.selectbox(
    'Daftar Menu',
    ('Home', 'Klasifikasi Individu', 'Klasifikasi Kelompok')
)

st.write("""
# Web Apps - Klasifikasi Waktu Kelulusan Mahasiswa
Aplikasi Berbasis Web untuk Mengklasifikasikan Waktu Kelulusan Mahasiswa
Magister Ilmu Komputer Universitas Brawijaya
""")

if option == 'Home' or option == '':
    st.header("Tentang Aplikasi")
    st.write("Aplikasi ini dibuat bertujuan untuk melakukan klasifikasi waktu kelulusan mahasiswa Magister Ilmu Komputer Universitas Brawijaya")
    st.write(
        "Proses klasifikasi dilakukan berdasarkan hasil seleksi masuk calon mahasiswa")
    st.write(
        "Data hasil seleksi yang akan digunakan mencakup 6 komponen penilaian antara lain : ")
    st.write("1. Nilai Interview")
    st.write("2. Nilai Setara TOEFL")
    st.write("3. Nilai TPA")
    st.write("4. Nilai Tes Bidang")
    st.write("5. Nilai Setara IPK")
    st.write("6. Rekomendasi Beasiswa")

    st.header("Fitur Aplikasi")
    st.write("Pada aplikasi ini terdapat 2 fitur yang dapat digunakan untuk melakukan proses klasifikasi yaitu : ")
    st.write("1. Klasifikasi Perorangan")
    st.write("2. Klasifikasi Kelompok")

elif option == 'Klasifikasi Individu':
    st.write(
        """## Klasifikasi Tunggal Mahasiswa""")  # menampilkan judul halaman dataframe
    st.write("Menu ini digunakan untuk melakukan prediksi tunggal kepada mahasiswa")
    st.write("Silakan mengisi secara lengap keperluan data di bawah ini")

    st.subheader('Nilai Administrasi Mahasiswa')
    nama_mhs = st.text_input('Nama mahasiswa')
    jenis_beasiswa = st.selectbox(
        'Jenis beasiswa mahasiswa',
        ('', 'Tidak menerima', 'Silver', 'Gold', 'Diamond'))
    bidang_riset = st.selectbox(
        'Bidang riset mahasiswa',
        ('', 'Teknologi Media, Game dan Piranti Bergerak', 'Jaringan Berbasis Informasi',
         'Rakayasa Perangkat Lunak', 'Sistem Cerdas', 'Sistem Informasi'))

    akreditas_kampus = st.selectbox(
        'Akreditasi kampus asal mahasiswa',
        ('', 'C / Baik', 'B / Baik Sekali', 'A / Unggul'))

    st.subheader('Nilai Tes Bidang')
    col1, col2 = st.columns([1, 1])
    nilai_matematika_komputasi = col1.slider(
        'Nilai matematika komputasi', 0.0, 100.0, 0.0)
    nilai_jaringan = col2.slider(
        'Nilai jaringan berbasis informasi', 0.0, 100.0, 0.0)

    col3, col4 = st.columns([1, 1])
    nilai_basis_data = col3.slider(
        'Nilai basis data', 0.0, 100.0, 0.0)
    nilai_algoritma = col4.slider(
        'Nilai algoritma dan pemrograman', 0.0, 100.0, 0.0)

    nilai_tes_bidang = st.slider('Nilai akhir tes bidang', 0.0, 100.0, 0.0)
    nilai_setara_IPK = st.slider('Nilai setara IPK', 0.0, 100.0, 0.0)

    st.subheader('Nilai Interview')
    col5, col6 = st.columns([1, 1])
    motivasi_studi = col5.slider(
        'Nilai motivasi studi', 0.0, 100.0, 0.0)
    motivias_beasiswa = col6.slider(
        'Nilai motivasi beasiswa', 0.0, 100.0, 0.0)

    col7, col8 = st.columns([1, 1])
    pengalaman = col7.slider(
        'Nilai pengalaman', 0.0, 100.0, 0.0)
    rencana_riset = col8.slider(
        'Nilai rencana riset', 0.0, 100.0, 0.0)

    col9, col10 = st.columns([1, 1])
    komunikasi = col9.slider(
        'Nilai komunikasi', 0.0, 100.0, 0.0)
    problem_solving = col10.slider(
        'Nilai probelm solving', 0.0, 100.0, 0.0)

    col11, col12 = st.columns([1, 1])
    literature_review = col11.slider(
        'Nilai literature review', 0.0, 100.0, 0.0)
    team_work = col12.slider(
        'Nilai team work', 0.0, 100.0, 0.0)
    nilai_interview = st.slider('Nilai akhir interview', 0.0, 100.0, 0.0)

    st.subheader('Nilai TOEFL')
    col13, col14 = st.columns([1, 1])
    jenis_TOEFL = col13.selectbox(
        'Jenis TOEFL mahasiswa',
        ('', 'Tidak ada', 'Preparation', 'iBT', 'ITP'))
    nilai_TOEFL = col14.slider(
        'Nilai setara TOEFL', 0.0, 100.0, 0.0)

    st.subheader('Nilai TPA')
    col15, col16 = st.columns([1, 1])
    jenis_TPA = col15.selectbox(
        'Jenis TPA mahasiswa',
        ('', 'Tidak ada', 'Lokal', 'OTO Bappenas'))
    nilai_TPA = col16.slider(
        'Nilai setara TPA', 0.0, 100.0, 0.0)

    nilai_total = st.slider('Nilai total administrasi', 0.0, 100.0, 0.0)
    st.markdown("""---""")

    # conver nilai
    np_jenis_beasiswa = 1
    if(jenis_beasiswa == ''):
        np_jenis_beasiswa = 1
    elif(jenis_beasiswa == 'Tidak menerima'):
        np_jenis_beasiswa = 1
    elif(jenis_beasiswa == 'Silver'):
        np_jenis_beasiswa = 2
    elif(jenis_beasiswa == 'Gold'):
        np_jenis_beasiswa = 3
    elif(jenis_beasiswa == 'Diamond'):
        np_jenis_beasiswa = 4

    np_bidang_riset = 1
    if(bidang_riset == ''):
        np_bidang_riset = 1
    elif(bidang_riset == 'Teknologi Media, Game dan Piranti Bergerak'):
        np_bidang_riset = 1
    elif(bidang_riset == 'Jaringan Berbasis Informasi'):
        np_bidang_riset = 2
    elif(bidang_riset == 'Rakayasa Perangkat Lunak'):
        np_bidang_riset = 3
    elif(bidang_riset == 'Sistem Cerdas'):
        np_bidang_riset = 4
    elif(bidang_riset == 'Sistem Informasi'):
        np_bidang_riset = 5

    nilai_matematika_komputasi = round(nilai_matematika_komputasi)
    nilai_jaringan = round(nilai_jaringan)
    nilai_basis_data = round(nilai_basis_data)
    nilai_algoritma = round(nilai_algoritma)
    nilai_tes_bidang = round(nilai_tes_bidang)
    nilai_setara_IPK = round(nilai_setara_IPK)

    np_akreditas_kampus = 1
    if(akreditas_kampus == ''):
        np_akreditas_kampus = 1
    elif(akreditas_kampus == 'C / Baik'):
        np_akreditas_kampus = 1
    elif(akreditas_kampus == 'B / Baik Sekali'):
        np_akreditas_kampus = 2
    elif(akreditas_kampus == 'A / Unggul'):
        np_akreditas_kampus = 3

    motivasi_studi = round(motivasi_studi)
    motivias_beasiswa = round(motivias_beasiswa)
    pengalaman = round(pengalaman)
    rencana_riset = round(rencana_riset)
    komunikasi = round(komunikasi)
    problem_solving = round(problem_solving)
    literature_review = round(literature_review)
    team_work = round(team_work)
    nilai_interview = round(nilai_interview)

    np_jenis_TOEFL = 1
    if(jenis_TOEFL == ''):
        np_jenis_TOEFL = 1
    elif(jenis_TOEFL == 'Tidak ada'):
        np_jenis_TOEFL = 1
    elif(jenis_TOEFL == 'Preparation'):
        np_jenis_TOEFL = 2
    elif(jenis_TOEFL == 'iBT'):
        np_jenis_TOEFL = 3
    elif(jenis_TOEFL == 'ITP'):
        np_jenis_TOEFL = 4
    nilai_TOEFL = round(nilai_TOEFL)

    np_jenis_TPA = 1
    if(jenis_TPA == ''):
        np_jenis_TPA = 1
    elif(jenis_TPA == 'Tidak ada'):
        np_jenis_TPA = 1
    elif(jenis_TPA == 'Lokal'):
        np_jenis_TPA = 2
    elif(jenis_TPA == 'OTO Bappenas'):
        np_jenis_TPA = 3
    nilai_TPA = round(nilai_TPA)

    nilai_total = round(nilai_total)

    data = np.array([[np_bidang_riset, nilai_matematika_komputasi,
                      nilai_jaringan, nilai_basis_data, nilai_algoritma,
                      nilai_tes_bidang, nilai_setara_IPK, np_akreditas_kampus,
                      motivasi_studi, pengalaman,
                      rencana_riset, komunikasi, problem_solving, literature_review,
                      team_work, nilai_interview, np_jenis_TOEFL, nilai_TOEFL,
                      nilai_TPA, nilai_total]])
    if st.button('Submit'):
        # build the scaler model
        # nilai maksimal
        dataBatas = np.array([[1, 0,
                               10, 10, 6.67,
                               18.34, 61.83, 1,
                               70, 60,
                               60, 60, 60, 0,
                               60, 66, 1, 20.74,
                               50, 48],
                              [5, 80,
                               80, 140, 140,
                               65.13, 95.50, 3,
                               90, 86,
                               90, 90, 90, 85,
                               90, 84, 4, 97,
                               113.34, 77.58]
                              ])
        combine = (np.vstack([dataBatas, data]))
        scaler = MinMaxScaler().fit(combine)
        ok = scaler.transform(combine)
        prediksi_tunggal = (model2.predict(np.delete(ok, (0, 1), axis=0)))
        proba = (model2.predict_proba(np.delete(ok, (0, 1), axis=0)))
        st.write("Klasifikasi Kelulusan Mahasiswa : ", prediksi_tunggal[0])
        if prediksi_tunggal[0] <= 4:
            st.header("Lulus Tepat Waktu")
        else:
            st.header("Tidak Lulus Tepat Waktu")
        st.write("Detail Probabilitas kelulusan")
        st.write("3 Semester : ", round(proba[0][0], 2))
        st.write("4 Semester : ", round(proba[0][1], 2))
        st.write("5 Semester : ", round(proba[0][2], 2))
        st.write("6 Semester : ", round(proba[0][3], 2))

elif option == 'Klasifikasi Kelompok':
    st.header("Klasifikasi Kelompok")
    st.write("Menu ini berfungsi untuk melakukan klasifkasi data kelompok mahasiswa")
    st.write(
        "Download file dibawah yang berisi template excel untuk dilakukan pengisian data")
    st.write("Pastikan mengganti tanda koma(,) dengan titik(.) sebelum file dimasukkan ke dalam kolom upload)
    st.write(
        "Template FIle Excel  -> [Download](https://drive.google.com/drive/folders/1lwhjMLOdy0YWe92FuiwJOZqTYBGndxcc?usp=sharing)")
    upload_file = st.file_uploader(
        "Pastikan file yang akan diupload telah sesuai dengan template file yang dibutuhkan!!!", type=["xlsx"])
    if upload_file is not None:
        df = pd.read_excel(upload_file)
        df0 = pd.DataFrame(df)
        st.subheader("Data Mahasiswa")
        st.write(df0)
        df1 = df.drop(['No', 'No. Pendaftaran', 'Nama Lengkap', 'Angkatan', 'Asal PT', 'Minor', 'Evaluator', 'Verifikator', 'Bobot TOEFL', 'Skor TOEFL', 'Nilai TOEFL', 'Reading', 'Speaking', 'Writing',
                       'Wawancara B. Ing', 'Bobot TPA', 'Skor TPA', 'Bobot', 'IPK', 'Tot Verbal', 'Tot Numeric', 'Tot Fig-Spa', 'Tot IQ', 'Klas', 'Nilai Psikotes', 'Nilai Total + Psikotes'], axis=1)
        nama = df[['Nama Lengkap', 'Angkatan']]
        df1.replace(
            to_replace="Teknologi Media Game dan Piranti Bergerak", value="1", inplace=True)
        df1.replace(to_replace="Jaringan Berbasis Informasi",
                    value="2", inplace=True)
        df1.replace(to_replace="Rakayasa Perangkat Lunak",
                    value="3", inplace=True)
        df1.replace(to_replace="Sistem Cerdas / Computer vision",
                    value="4", inplace=True)
        df1.replace(to_replace="Sistem Informasi", value="5", inplace=True)

        df1.replace(to_replace="Tidak ada", value="1", inplace=True)
        df1.replace(to_replace="Preparation", value="2", inplace=True)
        df1.replace(to_replace="iBT", value="3", inplace=True)
        df1.replace(to_replace="ITP", value="4", inplace=True)

        df1.replace(to_replace="Tidak ada", value="1", inplace=True)
        df1.replace(to_replace="Lokal", value="2", inplace=True)
        df1.replace(to_replace="OTO Bappenas", value="3", inplace=True)

        df1.replace(to_replace="C / Baik", value="1", inplace=True)
        df1.replace(to_replace="B / Baik Sekali", value="2", inplace=True)
        df1.replace(to_replace="A / Unggul", value="3", inplace=True)

        data = df1[['Mayor', 'Matematika_Komputasi', 'Jaringan_Komputer', 'Basis_Data', 'Algoritma_dan_Pemrograman', 'Nilai_Akhir_Tes_Bidang',
                    'Nilai_Setara_IPK', 'Status_PT', 'Motivasi_Studi', 'Motivasi_Beasiswa',
                    'Pengalaman_Penelitian', 'Rencana_Riset', 'Komunikasi',
                    'Problem_Solving', 'Literature_Review', 'Team_Work',
                    'Nilai_Akhir_Interview', 'Jenis_TOEFL', 'Nilai_Setara_TOEFL', 'Jenis_TPA',
                    'Nilai_TPA', 'Nilai_Total']]

        # build the scaler model
        data = pd.DataFrame(MinMaxScaler().fit_transform(data),
                            columns=data.columns, index=data.index)
        prediksi_kelompok = (model.predict(data))
        df_prediksi = pd.DataFrame(prediksi_kelompok, columns=['Lama_Kuliah'])
        df_prediksi.loc[df_prediksi['Lama_Kuliah']
                        == 3, 'Kelulusan'] = 'Tepat Waktu'
        df_prediksi.loc[df_prediksi['Lama_Kuliah']
                        == 4, 'Kelulusan'] = 'Tepat Waktu'
        df_prediksi.loc[df_prediksi['Lama_Kuliah']
                        == 5, 'Kelulusan'] = 'Tidak Tepat Waktu'
        df_prediksi.loc[df_prediksi['Lama_Kuliah']
                        == 6, 'Kelulusan'] = 'Tidak Tepat Waktu'
        df_prediksi.loc[df_prediksi['Lama_Kuliah']
                        == 7, 'Kelulusan'] = 'Tidak Tepat Waktu'
        row_prediksi = pd.concat(
            [nama, df_prediksi], axis=1)
        st.subheader("Hasil Prediksi Mahasiswa")
        st.write(row_prediksi)
        st.text('')
        df_xlsx = to_excel(row_prediksi)
        st.download_button(label='📥 Download hasil',
                           data=df_xlsx,
                           file_name='hasil_prediksi.xlsx')

        bar_chart1 = px.histogram(row_prediksi, x='Kelulusan', y=None,
                                  color='Angkatan', barmode='group',
                                  height=400)
        st.plotly_chart(bar_chart1)

        bar_chart2 = px.histogram(row_prediksi, x='Kelulusan', y=None,
                                  color='Lama_Kuliah', barmode='group',
                                  height=400)
        st.plotly_chart(bar_chart2)
