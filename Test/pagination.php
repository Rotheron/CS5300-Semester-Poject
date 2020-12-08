<html>
<head>
    <title>Pagination</title>
    <!-- Bootstrap CDN -->
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">
    <link rel="stylesheet" href="../CSS/pagination.css">
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.2.1/jquery.min.js"></script>
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js"></script>
</head>
<body>
    <?php
      $hostname = "cs-class-db.srv.mst.edu";
      $username = "cedtfh";
      $password = "koobpasswordkoobpassword2!";
      $db = "cedtfh";

      $dbconnect=mysqli_connect($hostname,$username,$password,$db);
        if (isset($_GET['pageno'])) {
            $pageno = $_GET['pageno'];
        } else {
            $pageno = 1;
        }
        $no_of_records_per_page = 25;
        $offset = ($pageno-1) * $no_of_records_per_page;


        $total_pages_sql  = "SELECT COUNT(*) FROM BOOKS as Book 
                            NATURAL JOIN AUTHOR_BOOK
                            JOIN AUTHOR on AUTHOR.AUTHOR_ID = AUTHOR_BOOK.Author_ID
                            JOIN BOOK_INFO on BOOK_INFO.Book_Info_ID = Book.Book_Info_ID
                            WHERE Book.Title IS NOT NULL
                            AND Book.Price IS NOT NULL";


        $result = mysqli_query($dbconnect,$total_pages_sql);
        $total_rows = mysqli_fetch_array($result)[0];
        $total_pages = ceil($total_rows / $no_of_records_per_page);

        $sql = "SELECT Book.Title, AUTHOR.Name, Book.Price, Book.Book_ID, BOOK_INFO.ISBN_10 FROM BOOKS as Book 
                    NATURAL JOIN AUTHOR_BOOK
                    JOIN AUTHOR on AUTHOR.AUTHOR_ID = AUTHOR_BOOK.Author_ID
                    JOIN BOOK_INFO on BOOK_INFO.Book_Info_ID = Book.Book_Info_ID
                    WHERE Book.Title IS NOT NULL
                    AND Book.Price IS NOT NULL
                    ORDER BY Book.Title
                    LIMIT $offset, $no_of_records_per_page ";

        if(!mysqli_query($dbconnect,$sql))
        {
            printf("Error: %s\n", mysqli_error($dbconnect));
            exit();
        }
    ?>


    <div id="allBookWrapper"> 
        <?php
            $res_data = mysqli_query($dbconnect,$sql);
            while($row = mysqli_fetch_array($res_data)){
                //here goes the data
                #$imgJSON=\"https://www.googleapis.com/books/v1/volumes?q=isbn:\"{$row[4]}
                #<img src={$imgJSON}> attempting some google books stuff but might not be needed
                echo
                "<div class=\"book\">
                    <img src=\"http://covers.openlibrary.org/b/isbn/{$row[4]}.jpg\" class=\"bookImg\">
                    <div class=\"bookText\">
                        <div><p>{$row[0]}</p></div>
                        <div><p>{$row[1]}</p></div>
                        <div><p>{$row[2]}</p></div> 
                        <div><p>{$row[3]}</p></div> 
                    </div>
                </div>";
            }
            mysqli_close($dbconnect);
        ?>
    </div>


    <ul class="pagination">
        <li><a href="?pageno=1">First</a></li>
        <li class="<?php if($pageno <= 1){ echo 'disabled'; } ?>">
            <a href="<?php if($pageno <= 1){ echo '#'; } else { echo "?pageno=".($pageno - 1); } ?>">Prev</a>
        </li>
        <li class="<?php if($pageno >= $total_pages){ echo 'disabled'; } ?>">
            <a href="<?php if($pageno >= $total_pages){ echo '#'; } else { echo "?pageno=".($pageno + 1); } ?>">Next</a>
        </li>
        <li><a href="?pageno=<?php echo $total_pages; ?>">Last</a></li>
    </ul>
</body>
</html>
