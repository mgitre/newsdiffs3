var DiffMatchPatch = require("diff-match-patch");

var tag_array = ["<p>","<h1>","<h2>","<h3>","<h4>","<h5>","<h6>","</p>","</h1>","</h2>","</h3>","</h4>","</h5>","</h6>"];
var diff_tags = ["del","ins"]

//replaces each html tag with a corresponding character code way out of range of anything plausible
function replace_html_tags(text){
    for (var i = 0; i < tag_array.length; i++){
        tag = tag_array[i]
        text = text.replace(new RegExp(tag, 'g'), String.fromCharCode(2048+i))
    }
    return text;
}

function reinsert_html_tags(text){
    for (var i = 0; i < tag_array.length; i++){
        tag = tag_array[i]
        text = text.replace(new RegExp(String.fromCharCode(2048+i), 'g'), tag)
    }
    return text;
}

//gets diffs from 2 inputs, and a cost
function get_diffs(original, newer, cost=12){
    var dmp = new DiffMatchPatch();
    var diff = dmp.diff_main(original, newer);
    dmp.Diff_EditCost = cost;
    dmp.diff_cleanupEfficiency(diff);
    return diff;
}

//gets html from those diffs. this is janky rn. please dont be mad :)
function get_html_from_diffs(diffs){
    var output='';
    for (const diff of diffs){
        //if the segment is the same across both texts, append without any fuckery
        var diff_type = diff[0];
        if (diff_type==0) {
            output += diff[1];
            continue;
        }
        //splits the text at all placeholder html tags, keeping them in the array
        //if adding more tags, adjust the regex accordingly
        var split = diff[1].split(/([\u0800-\u080d])/g);

        //iterate over each segment in split
        for (var i=0; i < split.length; i++){

            //if it's an html tag, don't fuck with it
            //this works because when splitting at a delimiter (while keeping
            //the delimiter) it alternates delimiters and content
            if (i%2==1){
                output += split[i];
            }
            //if it's not an html tag, fuck with it
            else {
                //this is janky as hell but who cares, i like it
                //maps difftype to what tag to use, since deletion is -1 and insertion is 1
                var diff_tag = diff_tags[(diff_type+1)/2];

                //wraps segment in relevant tags
                var segment = `<${diff_tag}>${split[i]}</${diff_tag}>`;
                output += segment;
            }
        }
    }

    //reinsert html tags
    return reinsert_html_tags(output);
}


//this wraps everything, when in doubt just use this lol
function get_nice_html_diff(text1, text2, cost=12){
    text1 = replace_html_tags(text1);
    text2 = replace_html_tags(text2);
    diffs = get_diffs(text1, text2, cost);
    pretty_html = get_html_from_diffs(diffs);
    return pretty_html;
}