# files/read_write.py
with open('dadams.txt') as f:
    lines = [line.rstrip() for line in f]
with open('dadams_copy.txt', 'w') as fw:
    fw.write('\n'.join(lines))
# Specify the size of each chunk to read
chunk_size = 16
with open('Slide3.PNG', 'rb') as file_:
  # Using while loop to iterate the file data
  while True:
      chunk = file_.read(chunk_size)
      if not chunk:
          break
      # Processing the chunk of binary data
      print(f'Read {len(chunk)} bytes: {chunk}')
