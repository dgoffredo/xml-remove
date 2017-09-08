
# Assume that xml-remove.py is in the parent directory of this one.
example_dir=$(dirname $(readlink -f "$0"))
script_dir=$(dirname $example_dir)

$script_dir/xml-remove.py '/Configuration/thing[text()="stuff"]' \
    < $example_dir/input.xml \
    > $example_dir/output.xml
