import os
import struct

def create(archive, folder):
	files = []
	for f in os.listdir(folder):          #переюираем всё что есть в папке
		full_path = os.path.join(folder, f)     #берём полный путь
		if os.path.isfile(full_path):           #это файл?
			files.append(f)
	with open(archive, "wb") as arc:                 #бинарный режим wb
		arc.write(struct.pack("I", len(files)))      #в архиватор записываем количество файлов (int)


		for f in files:
			filepath = os.path.join(folder, f)
			name_b = f.encode("utf-8")                   #имя в байтах
			arc.write(struct.pack("I", len(name_b)))     #пишем длину имени целым числом(int)
			arc.write(name_b)

			filesize = os.path.getsize(filepath)
			arc.write(struct.pack("Q", filesize))        #пишем размер файла большим числом(8 байт)

			with open(filepath, "rb") as f:
				arc.write(f.read())
	print(f"Архив {archive} создан. Файлов: {len(files)}")



def unpack(archive, folder):
	with open(archive, "rb") as arc:
		count = struct.unpack("I", arc.read(4))[0] #читаем количество файлов
		for i in range(count):
			name_len = struct.unpack("I", arc.read(4))[0] #длина имени
			name = arc.read(name_len).decode("utf-8")  #само имя
			filesize = struct.unpack("Q", arc.read(8))[0] #размер файла (Q так как размер может быть больше 4 гб тогда I не подойдёт) 
			content = arc.read(filesize)  #содержимое файла
			out_path = os.path.join(folder, name) #путь
			with open(out_path, "wb") as out:    # создаём файл на диске
				out.write(content)

	print(f"Архив {archive} распакован. Файлов: {count}")





create("test.arc", "/data/data/com.termux/files/home/test_folder")

unpack("test.arc", "/data/data/com.termux/files/home/test_unpacked")
