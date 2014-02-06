#!/usr/bin/ruby

#
# fixedf_runmulti.rb
# Run galcenbayes_fixedf for a range of values of magnetar fraction f.
#
# Usage: fixedf_runmulti.rb
#   Once this is run, the file survey.nvsf will contain the upper limit on N
#   for each magnetar fraction f.
#
# Created by Jayanth Chennamangalam
#

n = 100000
startf = 0.001
stepf = 0.010
stopf = 0.999

f = (startf..stopf).step(stepf).to_a
numf = f.length

%x[touch survey.nvsf]

for i in 0...numf
  %x[./galcenbayes_fixedf 0.050 4.85 -0.8 #{n} #{f[i]} >> survey.nvsf 2> /dev/null]
end

