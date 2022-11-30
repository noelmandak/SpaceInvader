# SpaceInvader

## Library eksernal yang digunakan:
* pygame
* kink
* matplotlib
* pylab
* smtplib
* pillow

## instal library eksternal:
```
pip install pygame
pip install kink
pip install matplotlib
pip install pylab
pip install smtplib
pip install pillow
```

## Cara menggunkakan Game Space Invader:
1. Ekstrak File Game Space Invader
2. Buka CMD atau terminal di Folder tempat game di ekstrak lalu jalankan game dengan cara 

    ```
    python -m SpaceInvader -db_init=False
    ```
  
5. Akan Muncul Jendela Permainan, Tekan apa saja atau klik layar jendela untuk masuk ke menu utama
6. Dalam Menu Utama terdapat 4 Tombol yaitu, New Player, Registered Player, Score Board, dan Quit(x)
7. Jika Pemain belum pernah melakukan registrasi, Tekan tombol New Player.

    * Isi kolom Username, Age, dan Email
    * Kolom Username hanya dapat diisi dengan huruf kecil, angka, dan simbol sperti !@#$%^&*()_+-=~:<>,.
    * Kolom Username hanya dapat diisi 10 karakter
    * Kolom Age hanya bisa di isi angka bulat positif
    * Kolom email dapat di isi dengan huruf kecil, angka, dan simbol sperti !@#$%^&*()_+-=~:<>,. tanpa batasan karakter
    * Jika sudah disi, tekan tanda > untuk melanjutkan ke halaman start permainan
    * Username bersifat unik, jadi jika username telah terdaftar, silahkan pilih username lain
  
6. Jika Pemain sudah pernah melakukan registrasi, Tekan tombol Registered Player.
    * Isi kolom Username
    * Kolom Username hanya dapat diisi dengan huruf kecil, angka, dan simbol sperti !@#$%^&*()_+-=~`:<>,.
    * Kolom Username hanya dapat diisi 10 karakter
    * Kalau sudah di isi, tanda > untuk melanjutkan ke halaman start permainan
    * Jika ternyata username belum pernah diregistrasi, anda perlu kembali ke menu utama dengan menekan tombol < , lalu meregistrasi diri anda
7. Tombol ScoreBoard untuk menapilkan rangking dari semua pemain terdaftar berdasarkan skor tertinggi mereka
8. Tombol quit (x) itu akan meminta konfirmasi, mau keluar atau tidak, kalau mau keluar tekan centang kalau batal tekan silang
9. Dalam Halaman start permainan, terdapat 3 tombol yaitu, back(<), play, dan player analytics
    * Jika tombol back(<) ditekan, maka akan kemabali ke menu utama
    * Jika tombol play ditekan maka akan masuk ke halaman in game
    * Jika tombol player analytics maka masuk ke halaman analisa player
10. Dalam halaman in game, 
    * Player dapat menggerakan suatu SpaceShip (pesawat luar angkasa) ke kiri dan ke kanan menggunakan arrow ← → dan menembak dengan menekan spasi
    * Terdapat alien yang bergerak ke kanan dan kekiri, dan jika alien mencapai ujung dia akan turun satu langkah
    * Misi Player adalah menjaga agar alien tidak mencapai garis putus-putus yang ada didepan SpaceShip dengan cara menembak alien-alien tersebut
    * SpaceShip hanya bisa menembakan satu peluru dalam satu waktu, dan dapat menembak lagi jika peluru mengenai alien atau hilang (keluar tampilan)
    * Jika player bisa menembak satu alien, maka player akan medapatkan tambahan 10 poin untuk skornya
    * Level akan bertambah jika score player bisa mencapai ratusan ganjil seperti 100, 300, 500 dst
    * Setiap kali level bertambah, kecepatan pesawat dan alien bertambah
    * Agar semakin seru, setiap kali player mencapai level dengan kelipatan 5, alien akan bertambah satu
    * Player bisa menekan tombol ⏸ atau tombol p pada keyboard untuk menjeda permainan
    * Pada saat permainan di jeda, player bisa menekan p atau ⏸ untuk melanjutkan atau juga bisa menekan tombol silang untuk menyerah
    * Jika alien menyentuh garis putus-putus atau player menyerah game akan berhenti (Game Over)
    * Pada saat Game Over, akan ada tampilan score dari game saat itu, highscore yang pernah didapatkan, jumlah alien yang mati, jumlah peluru yang dikeluarkan, akurasi dan durasi permainan
    * Setelah Game Over, tekan tombol > untuk kembali ke halaman start permainan
11. Dalam halaman analisa pemain,
    * Terdapat 4 tombol yang bisa dipilih yaitu, score, accuracy, enemy killed dan duration
    * Jika tombol tersebut ditekan, akan muncul history permainan pemain dalam bentuk diagram garis
    * Dengan visualisasi tersebut, pemain dapat menyusun strategi lagi untuk meningkatkan kemampuannya baik itu semakin besar skor, meningkatkan akurasi dan tambah tahan lama.
    * Player bisa kembali ke halaman Start permainan dengan cara menekan tombol back (<)

## Untuk pak sanga
Karena saya tidak bisa mendemokannya langsung, saya mengganti satu email player dari test saya menjadi email bapak, agar bisa tahu emailnya terkirim atau tidak.
Bagian yang saya ubah ada di test_highscore_board_must_return_all_player_highscore_descending_order(). Dalam test tersebut seperti ada 3 orang yang bermain bergantian, dan saat score sanga 200, sanga yang jadi rank 1, tapi saat score jabez 700 jabez dapat rank 1, dan sanga turun rank menjadi rank 2.
Saat test tersebut dijalankan seharusnya email sanga.lawalata@calvin.ac.id mendapatkan email berjudul "Your rank is down". 
Seharusnya itu bisa pake mock, tapi supaya bisa tahu terkirim atau tidak saya pake kirim email yang beneran.


## untuk melihat grafik analisa pemain, jalankan program dengan:
```
python -m SpaceInvader -db_init=demo
```
lalu registrasi dengan username "noel", lalu tekan player analytics
