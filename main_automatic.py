from tools import *

#[table_name, name, min_cc, max_cc, num]
searches =  [['kawasaki', 'kawasaki er6n', 600, 700, 100], 
            ['yamaha', 'yamaha mt07', 600, 700, 100], 
            ['suzuki', 'drz400', 350, 500, 100],
            ['yamaha', 'yamaha xt660', 600, 700, 100],
            ['KTM', 'KTM supermoto', 600, 700, 100]
            ]

for v in searches:
  offs = search(v[1], v[2], v[3], (v[4]))
  save(offs, v[0])