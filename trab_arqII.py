# Escreva uma função para extrair as informações da setor de boot (Master Bott Record) de um de um arquivo criado pelo HxD contendo 
# o conteúdo em memória de um pendrive FAT32.

# A função deve receber o nome do arquivo e retornar um dicionário com as seguintes informações:
# - Tamanho do setor em bytes
# - Tamanho do cluster em setores
# - Tamanho do setor de boot em setores
# - Tamanho da FAT em setores
# - Tamanho da FAT em bytes
# - Tamanho da área de dados em setores
# - Tamanho da área de dados em bytes
# - Numero total de clusters
# - Numero de setores por cluster

# O dicionário deve ter as chaves:
# - sector_size
# - cluster_size
# - boot_sector_size
# - fat_size
# - fat_size_bytes
# - data_area_size
# - data_area_size_bytes
# - total_clusters
# - sectors_per_cluster

# O dicionário deve ser retornado com os valores convertidos para inteiros.


def extract_boot_sector_info(file_name):
    with open(file_name, 'r') as file:
        data = file.read().split()

        sector_size = int(data[11], base=16) + 256 * int(data[12], base=16)
        cluster_size = int(data[13], base=16)

        # Tamanho da área reservada (em setores)
        boot_sector_size = int(data[14], base=16) + 256 * int(data[15], base=16)

        fat_copies_number = int(data[16], base=16)
        sectors_per_fat = int(data[22], base=16) + 256 * int(data[23], base=16)

        # Área dos arquivos (em setores)
        data_area_size = int(data[19], base=16) + 256 * int(data[20], base=16)
        if (data_area_size == 0):
            data_area_size = int(data[32], base=16) + 256 * int(data[33], base=16) + 256**2 * int(data[34], base=16) + 256**3 * int(data[35], base=16)

        data_area_size_bytes = data_area_size * sector_size
        total_clusters = data_area_size // cluster_size
        sectors_per_cluster = cluster_size

        fat_type = None

        root_dir_first_cluster = int(data[44], base=16) + 256 * int(data[45], base=16) + 256**2 * int(data[46], base=16) + 256**3 * int(data[47], base=16)

        if total_clusters < 4085:
            fat_type = 'FAT12'
        elif total_clusters < 65525:
            fat_type = 'FAT16'
        else:
            fat_type = 'FAT32'

        # fat_offset = sector_size * boot_sector_size

        return {
            'sector_size': sector_size,
            'cluster_size': cluster_size,
            'boot_sector_size': boot_sector_size,
            'fat_copies_number': fat_copies_number,
            'sectors_per_fat': sectors_per_fat,
            # 'fat_size': fat_size,
            # 'fat_size_bytes': fat_size_bytes,
            'data_area_size': data_area_size,
            'data_area_size_bytes': data_area_size_bytes,
            'total_clusters': total_clusters,
            'sectors_per_cluster': sectors_per_cluster,
            'fat_type': fat_type,
            'root_dir_first_cluster' : root_dir_first_cluster
        }
    
def main():
    file_name = 'boot_sector_hex.txt'
    print(extract_boot_sector_info(file_name))

if __name__ == '__main__':
    main()
    