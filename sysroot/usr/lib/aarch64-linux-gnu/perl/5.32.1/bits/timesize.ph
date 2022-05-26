require '_h2ph_pre.ph';

no warnings qw(redefine misc);

require 'bits/wordsize.ph';
eval 'sub __TIMESIZE () { &__WORDSIZE;}' unless defined(&__TIMESIZE);
1;
