function out = read_segmentation_bin(fpath)

fid = fopen(fpath, 'rb');
a = fread(fid);
fclose(fid);
b = de2bi(a,8);
b = b';
b = b(:);
out = reshape(b, [1280,800]);
out = out';
