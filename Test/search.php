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
        #if you search for title or bookID
        if (!empty($_POST["search"]) and ($_POST["search_param"] != "Name" and $_POST["search_param"] != "ISBN_10")){
            $search_value=$_POST["search"];
            $search_param=$_POST["search_param"];
            $sql = "SELECT Book.Title, AUTHOR.Name, Book.Price, Book.Book_ID, BOOK_INFO.ISBN_10 FROM BOOKS as Book 
                NATURAL JOIN AUTHOR_BOOK
                JOIN AUTHOR on AUTHOR.AUTHOR_ID = AUTHOR_BOOK.Author_ID
                JOIN BOOK_INFO on BOOK_INFO.Book_Info_ID = Book.Book_Info_ID
                WHERE Book.Title IS NOT NULL
                AND Book.Price IS NOT NULL
                AND lower(Book.$search_param) like lower('%$search_value%')
                ORDER BY Book.Title
                LIMIT $offset, $no_of_records_per_page";

        }#if you search by author
        else if (!empty($_POST["search"]) and $_POST["search_param"] == "Name" and $_POST["search_param"] != "ISBN_10"){
            $search_value=$_POST["search"];
            $search_param=$_POST["search_param"];
            $sql = "SELECT Book.Title, AUTHOR.Name, Book.Price, Book.Book_ID, BOOK_INFO.ISBN_10 FROM BOOKS as Book 
                NATURAL JOIN AUTHOR_BOOK
                JOIN AUTHOR on AUTHOR.AUTHOR_ID = AUTHOR_BOOK.Author_ID
                JOIN BOOK_INFO on BOOK_INFO.Book_Info_ID = Book.Book_Info_ID
                WHERE Book.Title IS NOT NULL
                AND Book.Price IS NOT NULL
                AND lower(AUTHOR.$search_param) like lower('%$search_value%')
                ORDER BY Book.Title
                LIMIT $offset, $no_of_records_per_page";
        }#if you search by isbn
        else if (!empty($_POST["search"]) and $_POST["search_param"] != "Name" and $_POST["search_param"] == "ISBN_10"){
            $search_value=$_POST["search"];
            $search_param=$_POST["search_param"];
            $sql = "SELECT Book.Title, AUTHOR.Name, Book.Price, Book.Book_ID, BOOK_INFO.ISBN_10 FROM BOOKS as Book 
                NATURAL JOIN AUTHOR_BOOK
                JOIN AUTHOR on AUTHOR.AUTHOR_ID = AUTHOR_BOOK.Author_ID
                JOIN BOOK_INFO on BOOK_INFO.Book_Info_ID = Book.Book_Info_ID
                WHERE Book.Title IS NOT NULL
                AND Book.Price IS NOT NULL
                AND lower(BOOK_INFO.$search_param) like lower('%$search_value%')
                ORDER BY Book.Title
                LIMIT $offset, $no_of_records_per_page";
        }#take you back to home page if you search for blank text box
        else if(empty($_POST["search"]) and !isset($_GET['pageno'])) {
            header('Location: pagination.php');
            exit; 
        }

        #if you are using the pagination buttons (GET requests)
        if(empty($_POST["search"])){
            $search_value = $_GET['search_value'];
            $search_param = $_GET['search_param'];
            #if you are searching for Book title or bookID
            if ($search_param != "Name" and $search_param != "ISBN_10"){
                $sql = "SELECT Book.Title, AUTHOR.Name, Book.Price, Book.Book_ID, BOOK_INFO.ISBN_10 FROM BOOKS as Book 
                NATURAL JOIN AUTHOR_BOOK
                JOIN AUTHOR on AUTHOR.AUTHOR_ID = AUTHOR_BOOK.Author_ID
                JOIN BOOK_INFO on BOOK_INFO.Book_Info_ID = Book.Book_Info_ID
                WHERE Book.Title IS NOT NULL
                AND Book.Price IS NOT NULL
                AND lower(Book.$search_param) like lower('%$search_value%')
                ORDER BY Book.Title
                LIMIT $offset, $no_of_records_per_page";
            }#if you are searching for author name
            else if($search_param == "Name"){
                $sql = "SELECT Book.Title, AUTHOR.Name, Book.Price, Book.Book_ID, BOOK_INFO.ISBN_10 FROM BOOKS as Book 
                NATURAL JOIN AUTHOR_BOOK
                JOIN AUTHOR on AUTHOR.AUTHOR_ID = AUTHOR_BOOK.Author_ID
                JOIN BOOK_INFO on BOOK_INFO.Book_Info_ID = Book.Book_Info_ID
                WHERE Book.Title IS NOT NULL
                AND Book.Price IS NOT NULL
                AND lower(AUTHOR.$search_param) like lower('%$search_value%')
                ORDER BY Book.Title
                LIMIT $offset, $no_of_records_per_page";
            }#if you are searching for isbn
            else if($search_param == "ISBN_10"){
                $sql = "SELECT Book.Title, AUTHOR.Name, Book.Price, Book.Book_ID, BOOK_INFO.ISBN_10 FROM BOOKS as Book 
                NATURAL JOIN AUTHOR_BOOK
                JOIN AUTHOR on AUTHOR.AUTHOR_ID = AUTHOR_BOOK.Author_ID
                JOIN BOOK_INFO on BOOK_INFO.Book_Info_ID = Book.Book_Info_ID
                WHERE Book.Title IS NOT NULL
                AND Book.Price IS NOT NULL
                AND lower(BOOK_INFO.$search_param) like lower('%$search_value%')
                ORDER BY Book.Title
                LIMIT $offset, $no_of_records_per_page";
            }
        }

        //Get # of rows returned for whatever query we're running
        $sql2 = substr($sql, 0, strpos($sql, "LIMIT"));     //Make sql2 return all rows, not the $offset we have above (that's for pagination and stuff...)
        $result = mysqli_query($dbconnect,$sql2);
        $total_rows = mysqli_num_rows($result); 
        $total_pages = ceil($total_rows / $no_of_records_per_page);
        if(!mysqli_query($dbconnect,$sql))
        {
            printf("Error: %s\n", mysqli_error($dbconnect));
            exit();
        }
    ?>

    <div id="searchWrapper">
        <form action="search.php" method="post">
        <input id="search" name="search" type="text" placeholder="Type here">
        <input id="submit" type="submit" value="Search">
        <select id="search_param" name="search_param">
            <option value="Title">Title</option>
            <option value="Name">Author</option>
            <option value="Book_ID">Book ID</option>
            <option value="ISBN_10">ISBN</option>
        </select>
        </form>

    </div>

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
        <li><a href="?pageno=1<?php echo "&search_value=".$search_value."&search_param=".$search_param;?>">First</a></li>
        <li class="<?php if($pageno <= 1){ echo 'disabled'; } ?>">
            <a href="<?php if($pageno <= 1){ echo '#'; } else { echo "?pageno=".($pageno - 1)."&search_value=".$search_value."&search_param=".$search_param; } ?>">Prev</a>
        </li>

        <!-- Dynamically Generate the "in-between" pagination numbers -->
        <?php
            for ($i=2; $i<=$total_pages; $i++)
            {
                echo "<li><a href=\"?pageno=".$i."&search_value=".$search_value."&search_param=".$search_param."\">".$i."</a></li>";
            }
        ?>

        <li class="<?php if($pageno >= $total_pages){ echo 'disabled'; } ?>">
            <a href="<?php if($pageno >= $total_pages){ echo '#'; } else { echo "?pageno=".($pageno + 1)."&search_value=".$search_value."&search_param=".$search_param; } ?>">Next</a>
        </li>
        <li><a href="?pageno=<?php echo $total_pages."&search_value=".$search_value."&search_param=".$search_param;?>">Last</a></li>
    </ul>
</body>
</html>
