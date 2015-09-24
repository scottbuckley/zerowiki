<?php
    
    // note that this should be placed in a __zwheader folder!
    
    // parameters
    $dir     = '../';
    $dumpf   = '.zwdump';
    $qstring = $_SERVER['QUERY_STRING'];


    // helper for string operations
    function endsWith($haystack, $needle) {
        return $needle === '' || substr_compare($haystack, $needle, -strlen($needle)) === 0;
    }


    // load dump from file
    @$dump = unserialize(file_get_contents($dumpf));
    if (!$dump) {
        $dump = array();
    }


    // get a list of all the files
    $files   = array_filter(scandir($dir), function($file) use (&$dir) {
        if (endsWith($file, '.md'))
            if (is_file($dir . $file))
                return true;
        return false;
    });


    // update dump
    $updateCount = 0;
    foreach ($files as $file) {
        if (!array_key_exists($file, $dump))
            $dump[$file] = array('lastchecked' => 0);

        // if file is change since last check...
        $date_checked  = $dump[$file]['lastchecked'];
        $date_modified = filemtime($dir.$file);
        if ($date_modified > $date_checked) {

            // read file
            $filecont = file_get_contents($dir.$file);

            // get internal links
            preg_match_all('/\]\(([^\)]+?\.md)(?:\#[^\)]*?)?\)/', $filecont, $matches);
            
            // save to dump
            $dump[$file]['links'] = $matches[1];
            $dump[$file]['lastchecked'] = time();
            $updateCount += 1;
        }
    }

    // save dump to file
    if ($updateCount > 0) {
        file_put_contents($dumpf, serialize($dump));
    }

    // process references
    $reflinks = array();
    foreach ($dump as $file => $properties) {
        if (in_array($qstring, $properties['links'])) {
            $reflink = '[' . $file . '](?' . $file . ')';
            $reflinks[] = $reflink;
        }
    }

    // process output
    if (count($reflinks) > 0) {
        echo '<div class="zwheader" style="position: absolute; left: 2em; top: 2em;">';
        echo 'Referenced by: ';
        echo join(', ', $reflinks);
        echo '</div>';
    }

?>