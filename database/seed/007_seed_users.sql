INSERT INTO users (name, email, password_hash)
VALUES
    (
        'Demo Admin',
        'george@grafeio.example',
        'scrypt:32768:8:1$95kUcLuJp1ky0Vma$0cee734226a9175f08a2522b04d5e3fbabcd9f93f7fc401d047d1f794533cfc602ec25f119c7e737de2e6f7bf900cfcb446faf5ba08e43cb1213e3b324df5079'
    ),
    (
        'Demo Employee 1',
        'employee1@grafeio.example',
        'scrypt:32768:8:1$P4iIeGeCpir3HgAL$4c0d51620a552d631a32a26e9457aaafbce62209a84e8b03f93f25480ff810c242477b666528d03030449067b8564c45b1e8e3ec659cc23a565b9555afa374c4'

    ),
    (
        'Demo Employee 2',
        'employee2@grafeio.example',
        'scrypt:32768:8:1$1KXXcBN3S4QNiCje$16cefba81656a78a62cd4640ee917144dcb3062a79c5d5c3985061066505ea2155d70766fbe9be07008912243705f8d4ca0f3a5d82eb22a0182ade7a8828949b'
    );