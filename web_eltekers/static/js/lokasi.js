document.addEventListener('DOMContentLoaded', function() {
    const selectProvinsi = document.getElementById('id_provinsi');
    const selectKota = document.getElementById('id_kota_kabupaten'); 
    const selectKecamatan = document.getElementById('id_kecamatan');
    const selectKelurahan = document.getElementById('id_kelurahan');

    function initForm() {
        selectKota.innerHTML = '<option value="">Pilih Kota/Kabupaten</option>';
        selectKecamatan.innerHTML = '<option value="">Pilih Kecamatan</option>';
        selectKelurahan.innerHTML = '<option value="">Pilih Kelurahan</option>';

        fetch(`https://www.emsifa.com/api-wilayah-indonesia/api/provinces.json`)
            .then(response => response.json())
            .then(provinces => {
                let options = '<option value="">Pilih Provinsi</option>';
                provinces.forEach(element => {
                    options += `<option data-reg="${element.id}" value="${element.name}">${element.name}</option>`;
                });
                selectProvinsi.innerHTML = options;

                if (typeof savedLocation !== 'undefined' && savedLocation.provinsi) {
                    selectProvinsi.value = savedLocation.provinsi;
                    selectProvinsi.dispatchEvent(new Event('change'));
                }
            })
            .catch(error => console.error('Error fetching provinsi:', error));
    }

    selectProvinsi.addEventListener('change', (e) => {
        selectKota.innerHTML = '<option value="">Pilih Kota/Kabupaten</option>';
        selectKecamatan.innerHTML = '<option value="">Pilih Kecamatan</option>';
        selectKelurahan.innerHTML = '<option value="">Pilih Kelurahan</option>';
        
        const provinsiId = e.target.options[e.target.selectedIndex].dataset.reg;
        if (provinsiId) {
            fetch(`https://www.emsifa.com/api-wilayah-indonesia/api/regencies/${provinsiId}.json`)
                .then(response => response.json())
                .then(regencies => {
                    let options = '<option value="">Pilih Kota/Kabupaten</option>';
                    regencies.forEach(element => {
                        options += `<option data-dist="${element.id}" value="${element.name}">${element.name}</option>`;
                    });
                    selectKota.innerHTML = options;

                    if (typeof savedLocation !== 'undefined' && savedLocation.kota) {
                        selectKota.value = savedLocation.kota;
                        selectKota.dispatchEvent(new Event('change'));
                    }
                });
        }
    });

    selectKota.addEventListener('change', (e) => {
        selectKecamatan.innerHTML = '<option value="">Pilih Kecamatan</option>';
        selectKelurahan.innerHTML = '<option value="">Pilih Kelurahan</option>';

        const kotaId = e.target.options[e.target.selectedIndex].dataset.dist;
        if (kotaId) {
            fetch(`https://www.emsifa.com/api-wilayah-indonesia/api/districts/${kotaId}.json`)
                .then(response => response.json())
                .then(districts => {
                    let options = '<option value="">Pilih Kecamatan</option>';
                    districts.forEach(element => {
                        options += `<option data-vill="${element.id}" value="${element.name}">${element.name}</option>`;
                    });
                    selectKecamatan.innerHTML = options;

                    if (typeof savedLocation !== 'undefined' && savedLocation.kecamatan) {
                        selectKecamatan.value = savedLocation.kecamatan;
                        selectKecamatan.dispatchEvent(new Event('change'));
                    }
                });
        }
    });

    selectKecamatan.addEventListener('change', (e) => {
        selectKelurahan.innerHTML = '<option value="">Pilih Kelurahan</option>';

        const kecamatanId = e.target.options[e.target.selectedIndex].dataset.vill;
        if (kecamatanId) {
            fetch(`https://www.emsifa.com/api-wilayah-indonesia/api/villages/${kecamatanId}.json`)
                .then(response => response.json())
                .then(villages => {
                    let options = '<option value="">Pilih Kelurahan</option>';
                    villages.forEach(element => {
                        options += `<option value="${element.name}">${element.name}</option>`;
                    });
                    selectKelurahan.innerHTML = options;

                    if (typeof savedLocation !== 'undefined' && savedLocation.kelurahan) {
                        selectKelurahan.value = savedLocation.kelurahan;
                        savedLocation.kelurahan = null; 
                    }
                });
        }
    });
    
    initForm();
});