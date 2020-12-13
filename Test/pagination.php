<html>
<head>
    <title>Pagination</title>
    <!-- Bootstrap CDN -->
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">
    <link rel="stylesheet" href="../Libraries/Glider.js-master/glider.css">
    <link rel="stylesheet" href="../font-awesome/css/font-awesome.min.css">
    <link rel="stylesheet" href="../CSS/pagination.css">
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.2.1/jquery.min.js"></script>
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js"></script>
        <script src="../Libraries/Glider.js-master/glider.js"></script>
    <script src="../Scripts/my_script.js"></script>
</head>
<body>
<script src="http://code.jquery.com/jquery.js"></script>
<script type="text/javascript">
var modal = document.getElementById("myModal");
var span = document.getElementsByClassName("close");
var book = document.getElementsByClassName("book");
 function bookClick(BookID){
    // var modal = document.getElementById("myModal");
    // modal.style.display = "block";
    
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            var modal = document.getElementById("myModal");
            modal.style.display = "block";
            modal.innerHTML = this.responseText;
        }        
    };

    var getMe = $(BookID).find('.bookID').text()
    xhttp.open("GET", "book_info.php?BookID="+getMe, true);
    xhttp.send();
}
 function spanClick(){
    var modal = document.getElementById("myModal");
    var span = document.getElementsByClassName("close");
    modal.style.display = "none";
}
window.onclick = function(event){
    var modal = document.getElementById("myModal");
    if(event.target == modal){
        modal.style.display = "none";
    }
}
</script>
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

    <div id="searchWrapper">
        <form action="search.php" method="post" class="search" id="search">
        <input id="search" name="search" class="searchTerm" type="text" placeholder="Type here">
        <button type="submit" form="search" class="searchButton">
            <i class="fa fa-search"></i>
        </button>
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
            #if the search button has been clicked, change the query to search
            $res_data = mysqli_query($dbconnect,$sql);
            while($row = mysqli_fetch_array($res_data)){
                //here goes the data
                #$imgJSON=\"https://www.googleapis.com/books/v1/volumes?q=isbn:\"{$row[4]}
                #<img src={$imgJSON}> attempting some google books stuff but might not be needed
                echo
                "<div class=\"book\" onclick=\"bookClick(this)\">
                    <img src=\"http://covers.openlibrary.org/b/isbn/{$row[4]}.jpg\" class=\"bookImg\">
                    <div class=\"bookText\">
                        <div><p>{$row[0]}</p></div>
                        <div><p>{$row[1]}</p></div>
                        <div><p>{$row[2]}</p></div> 
                        <div><p class=\"bookID\">{$row[3]}</p></div> 
                    </div>
                </div>";
            }
        ?>
    </div>
    <div id="myModal" class="modal">
    <!-- Modal content -->
        <div class="modal-content">
            <span class="close" onclick="spanClick()">&times;</span>
        </div>
    </div>

    <ul class="pagination">
        <!-- <li><a href="?pageno=1">First</a></li>
        <li class="<?php if($pageno <= 1){ echo 'disabled'; } ?>">
            <a href="<?php if($pageno <= 1){ echo '#'; } else { echo "?pageno=".($pageno - 1); } ?>">Prev</a>
        </li> -->
<!-- 
        <li class="<?php if($pageno >= $total_pages){ echo 'disabled'; } ?>">
            <a href="<?php if($pageno >= $total_pages){ echo '#'; } else { echo "?pageno=".($pageno + 1); } ?>">Next</a>
        </li>
        <li><a href="?pageno=<?php echo $total_pages; ?>">Last</a></li> -->
    </ul>



    <div class="glider-contain">
        <div class="glider">
        <!-- Dynamically Generate the "in-between" pagination numbers -->
            <?php
                for ($i=1; $i<=$total_pages; $i++)
                {
                    echo "<div class=\"pagination_link_wrapper\">";
                    echo "<a class=\"pagination_link\" href=\"?pageno=".$i."\">".$i."</a></div>\n";
                }
            ?> 
        </div>
        
            <!-- <button aria-label="Previous" class="glider-prev">«</button>
            <button aria-label="Next" class="glider-next">»</button> -->
            <div role="tablist" class="dots"></div>
    </div>

<?php mysqli_close($dbconnect); ?>
</body>
</html>
