$pdf_mode = 5;
$out_dir = 'build';
$aux_dir = 'build';
$max_repeat = 5;
$recorder = 1;

$xelatex = 'xelatex -file-line-error -halt-on-error -interaction=nonstopmode -synctex=1 %O %S';
$bibtex = 'bibtex %O %B';

$clean_ext = 'acn acr alg aux bbl bcf blg brf fdb_latexmk fls glg glo gls ist lof log lot out run.xml synctex.gz toc xdv';

add_cus_dep('glo', 'gls', 0, 'makeglossaries');
sub makeglossaries {
  return system("makeglossaries \"$_[0]\"");
}
