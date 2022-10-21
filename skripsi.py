import streamlit as st
import numpy as np
import pandas as pd
import pickle
import plotly.express as px


from sklearn.naive_bayes import GaussianNB


st.write("""
# Web Apps - Klasifikasi Waktu Kelulusan Mahasiswa
Aplikasi Berbasis Web untuk Mengklasifikasikan Waktu Kelulusan Mahasiswa
Magister Ilmu Komputer Universitas Brawijaya
""")

st.sidebar.image('logo_magister.png')


pilih_menu = st.sidebar.selectbox(
    "Menu", ("Home", "Klasifikasi Individu", "Klasifikasi Kelompok"))

if pilih_menu == "Home":
    st.title("Tentang Aplikasi")
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

if pilih_menu == "Klasifikasi Individu":
    Bidang_Minat = st.selectbox('Bidang Minat', ("Rakayasa Perangkat Lunak", "Teknologi Media, Game dan Piranti Bergerak",
                                                 "Sistem Cerdas", "Jaringan Berbasis Informasi", "Sistem Informasi"))
    Jenis_TOEFL = st.selectbox(
        'Jenis TOEFL', ("Tidak Ada", "Preparation", "iBT", "ITP"))
    Nilai__Setara_TOEFL = st.slider('Nilai Setara TOEFL', 40, 105, 65)
    Jenis_TPA = st.selectbox(
        'Jenis TPA', ("Tidak Ada", "Lokal", "OTO Bappenas"))
    Nilai_TPA = st.slider('Nilai TPA', 0, 120, 50)
    Akreditasi_Kampus = st.selectbox(
        'Akreditasi Kampus Asal', ("Swasta Biasa", "Swasta Non Unggulan", "Negeri Non Unggulan", "Swasta Unggulan", "Negeri Unggulan"))
    Nilai_Setara_IPK = st.slider('Nilai Setara IPK', 50, 100, 75)
    Jenis_Beasiswa = st.selectbox(
        'Jenis Beasiswa', ("Tidak", "Silver", "Gold", "Diamond"))
    col1, col2 = st.columns(2)
    Nilai_Total = st.slider('Nilai Total', 40, 85, 60)

    with col1:
        st.write("Nilai Interview")
        Motivasi_Studi = st.slider('Motivasi Studi', 50, 90, 70)
        Motivasi_Beasiswa = st.slider('Motivasi Beasiswa', 70, 90, 80)
        Pengalaman_Penelitian = st.slider('Pengalaman Penelitian', 50, 90, 70)
        Rencana_Riset = st.slider('Rencana Riset', 50, 90, 70)
        Komunikasi = st.slider('Komunikasi', 50, 90, 70)
        Problem_Solving = st.slider('Problem Solving', 50, 90, 70)
        Literatur_Review = st.slider('Literatur Review', 50, 90, 70)
        Team_Work = st.slider('Team Work', 50, 80, 70)
        Nilai_Total_Interview = st.slider('Nilai Total Interview', 50, 90, 70)

    with col2:
        st.write("Nilai Tes Bidang")
        Matematika_Komputasi = st.slider('Matematika Komputasi', 0, 65, 30)
        Jaringan = st.slider('Jaringan', 0, 65, 30)
        Basis_Data = st.slider('Basis Data', 0, 95, 50)
        Algoritma_dan_Pemrograman = st.slider(
            'Algoritma dan Pemrograman', 0, 95, 50)
        Nilai_Tes_Bidang = st.slider('Nilai Tes Bidang', 15, 80, 45)

        def user_input_features(
                Bidang_Minat,
                Motivasi_Studi,
                Motivasi_Beasiswa,
                Pengalaman_Penelitian,
                Rencana_Riset,
                Komunikasi,
                Problem_Solving,
                Literatur_Review,
                Team_Work,
                Nilai_Total_Interview,
                Jenis_TOEFL,
                Nilai__Setara_TOEFL,
                Jenis_TPA,
                Nilai_TPA,
                Matematika_Komputasi,
                Jaringan,
                Basis_Data,
                Algoritma_dan_Pemrograman,
                Nilai_Tes_Bidang,
                Akreditasi_Kampus,
                Nilai_Setara_IPK,
                Jenis_Beasiswa,
                Nilai_Total):
            data = {
                'Bidang_Minat': convert_bidangriset(Bidang_Minat),
                'Motivasi_Studi': Motivasi_Studi,
                'Motivasi_Beasiswa': Motivasi_Beasiswa,
                'Pengalaman_Penelitian': Pengalaman_Penelitian,
                'Rencana_Riset': Rencana_Riset,
                'Komunikasi': Komunikasi,
                'Problem_Solving': Problem_Solving,
                'Literatur_Review': Literatur_Review,
                'Team_Work': Team_Work,
                'Nilai_Total_Interview': Nilai_Total_Interview,
                'Jenis_TOEFL': convert_jenistoefl(Jenis_TOEFL),
                'Nilai__Setara_TOEFL': Nilai__Setara_TOEFL,
                'Jenis_TPA': convert_jenistpa(Jenis_TPA),
                'Nilai_TPA': Nilai_TPA,
                'Matematika_Komputasi': Matematika_Komputasi,
                'Jaringan': Jaringan,
                'Basis_Data': Basis_Data,
                'Algoritma_dan_Pemrograman': Algoritma_dan_Pemrograman,
                'Nilai_Tes_Bidang':  Nilai_Tes_Bidang,
                'Akreditasi_Kampus': convert_akreditasi(Akreditasi_Kampus),
                'Nilai_Setara_IPK': Nilai_Setara_IPK,
                'Jenis_Beasiswa': convert_beasiswa(Jenis_Beasiswa),
                'Nilai_Total': Nilai_Total}
            features = pd.DataFrame(data, index=[0])
            return features

        def convert_akreditasi(val):
            if val == "Swasta Biasa":
                return 1
            elif val == "Swasta Non Unggulan":
                return 2
            elif val == "Negeri Non Unggulan":
                return 3
            elif val == "Swasta Unggulan":
                return 4
            elif val == "Negeri Unggulan":
                return 5

        def convert_beasiswa(val):
            if val == "Tidak":
                return 1
            elif val == "Silver":
                return 2
            elif val == "Gold":
                return 3
            elif val == "Diamond":
                return 4

        def convert_bidangriset(val):
            if val == "Rakayasa Perangkat Lunak":
                return 1
            elif val == "Teknologi Media, Game dan Piranti Bergerak":
                return 2
            elif val == "Sistem Cerdas":
                return 3
            elif val == "Jaringan Berbasis Informasi":
                return 4
            elif val == "Sistem Informasi":
                return 5

        def convert_jenistpa(val):
            if val == "Tidak Ada":
                return 1
            elif val == "Lokal":
                return 2
            elif val == "OTO Bappenas":
                return 3

        def convert_jenistoefl(val):
            if val == "Tidak Ada":
                return 1
            elif val == "Preparation":
                return 2
            elif val == "iBT":
                return 3
            elif val == "ITP":
                return 4
    if st.button('Submit'):
        st.subheader('Data Input')
        df = user_input_features(
            Bidang_Minat,
            Motivasi_Studi,
            Motivasi_Beasiswa,
            Pengalaman_Penelitian,
            Rencana_Riset,
            Komunikasi,
            Problem_Solving,
            Literatur_Review,
            Team_Work,
            Nilai_Total_Interview,
            Jenis_TOEFL,
            Nilai__Setara_TOEFL,
            Jenis_TPA,
            Nilai_TPA,
            Matematika_Komputasi,
            Jaringan,
            Basis_Data,
            Algoritma_dan_Pemrograman,
            Nilai_Tes_Bidang,
            Akreditasi_Kampus,
            Nilai_Setara_IPK,
            Jenis_Beasiswa,
            Nilai_Total)

        st.write(df)
        load_model = pickle.load(open('modelnb.pkl', 'rb'))

        prediksi = load_model.predict(df)
        prediksi_proba = load_model.predict_proba(df)

        st.subheader('Keterangan Label Kelas')
        Kategori_Lulus = np.array(
            ['Lulus Tepat Waktu', 'Tidak Lulus Tepat Waktu'])
        st.write(Kategori_Lulus[prediksi])

        st.subheader('Probabilitas Prediksi')
        st.write("Probabilitas Lulus Tepat Waktu :")
        st.write(prediksi_proba[0][0]*100)
        st.write("Probabilitas tidak lulus tepat waktu")
        st.write(prediksi_proba[0][1]*100)

if pilih_menu == "Klasifikasi Kelompok":
    st.header("Klasifikasi Kelompok")
    st.write("Download template file excel pada link ini")
    st.write("")
    upload_file = st.file_uploader("Upload file disini", type=["xlsx"])
    if upload_file is not None:
        df = pd.read_excel(upload_file)
        st.write(df)
        input_kelompok = df.drop(['Nama_Lengkap', 'Angkatan'], axis=1)
        nama = df[['Nama_Lengkap', 'Angkatan']]
        load_model = pickle.load(open('modelnb.pkl', 'rb'))
        prediksi = load_model.predict(input_kelompok)
        prediksi_proba = load_model.predict_proba(input_kelompok)

        st.subheader('Hasil Klasifikasi')
        Kategori_Lulus = np.array(
            ['Lulus Tepat Waktu', 'Tidak Lulus Tepat Waktu'])
        label = (Kategori_Lulus[prediksi])
        klasifikasi = pd.DataFrame(label, columns=['Kategori_Lulus'])
        kelompok = pd.concat([nama, klasifikasi], axis=1)
        st.write(kelompok)

        bar_chart2 = px.histogram(kelompok, x='Kategori_Lulus', y=None,
                                  color='Angkatan', barmode='group',
                                  height=400)
        st.plotly_chart(bar_chart2)

    else:
        st.write("Masukkan file excel yang ingin dimasukkan")
