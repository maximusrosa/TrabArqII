from math import ceil, floor;


def deserialize(dataBytes, offset, numBytes):
    value = 0
    for i in range(numBytes):
        value += int(dataBytes[offset + i], base=16) * 256 ** i
    return value


def get_boot_sector_info(file_name):
    """
    Recupera informações de um arquivo de texto contendo os bytes (na base hexadecimal) 
    do setor de inicialização de um dispositivo de armazenamento.

    Args:
        file_name (str): O nome do arquivo.

    Returns:
        dict: Um dicionário contendo as seguintes informações:
            - bytesPerSector (int): Número de bytes por setor.
            - sectorsPerCluster (int): Número de setores por cluster.
            - bytesPerCluster (int): Número de bytes por cluster.
            - numSectorsReservedArea (int): Número de setores na área reservada.
            - numFATCopies (int): Número de cópias da FAT.
            - numEntriesRootDir (int): Número de entradas no diretório raiz.
            - numSectorsRootDir (int): Número de setores no diretório raiz.
            - sectorsPerFAT (int): Número de setores por FAT.
            - numHiddenSectors (int): Número de setores ocultos.
            - numTotalSectors (int): Número total de setores.
            - numSectorsFileArea (int): Número de setores na área de arquivos.
            - numTotalClusters (int): Número total de clusters na área de arquivos.
            - FATType (int): Tipo da FAT (12, 16 ou 32).
    """
    with open(file_name, 'r') as file:
        data = file.read().split()

        # Número de bytes por setor
        bytesPerSector = deserialize(data, 0x0b, 2)

        # Números de setores por cluster
        sectorsPerCluster = deserialize(data, 0x0d, 1)

        # Número de bytes por cluster
        bytesPerCluster = sectorsPerCluster * bytesPerSector

        # Número de setores da área reservada
        numSectorsReservedArea = deserialize(data, 0x0e, 2)

        # Número de cópias da FAT
        numFATCopies = deserialize(data, 0x10, 1)

        # Número de entradas no diretório raiz
        numEntriesRootDir = deserialize(data, 0x11, 2)

        # Número de setores no diretório raiz (calculado como descrito na especificação)
        numSectorsRootDir = ceil(((numEntriesRootDir * 32) + (bytesPerSector - 1)) / bytesPerSector)

        # Número de setores por FAT
        sectorsPerFAT = deserialize(data, 0x16, 2)

        # Número de setores ocultos
        numHiddenSectors = deserialize(data, 0x1c, 2)

        # Número total de setores
        numTotalSectors = deserialize(data, 0x13, 2)
        if numTotalSectors == 0:
            numTotalSectors = deserialize(data, 0x20, 4)

        # Número do primeiro setor de dados
        firstDataSector = numSectorsReservedArea + 2 * sectorsPerFAT + numSectorsRootDir

        # Número de setores da área de arquivos
        numSectorsFileArea = numTotalSectors - firstDataSector

        # Número total de clusters (somente área de arquivos)
        numTotalClusters = floor(numSectorsFileArea / sectorsPerCluster)

        FATType = None

        if numTotalClusters < 4085:
            # FAT12: número de clusters menor que 4085
            FATType = 12
        elif numTotalClusters < 65525:
            # FAT16: número de clusters no intervalo [4085; 65525)
            FATType = 16
        else:
            # FAT32: número de clusters maior que 65525
            FATType = 32

        return {
            'bytesPerSector': bytesPerSector,
            'sectorsPerCluster': sectorsPerCluster,
            'bytesPerCluster': bytesPerCluster,
            'numSectorsReservedArea': numSectorsReservedArea,
            'numFATCopies': numFATCopies,
            'numEntriesRootDir': numEntriesRootDir,
            'numSectorsRootDir': numSectorsRootDir,
            'sectorsPerFAT': sectorsPerFAT,
            'numHiddenSectors': numHiddenSectors,
            'numTotalSectors': numTotalSectors,
            'numSectorsFileArea': numSectorsFileArea,
            'numTotalClusters': numTotalClusters,
            'FATType': FATType,
        }


if __name__ == '__main__':
    print ('\n')
    for info, value in get_boot_sector_info('boot_sector_bytes.txt').items():
        print(f'{info}: {value}')
    print ('\n')
