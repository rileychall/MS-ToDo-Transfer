javascript: (function() {
    /* Download string formatted according to Blob content type */
    function download(content, fileName, contentType) {
        /* https://stackoverflow.com/a/34156339 */
        var a = document.createElement("a");
        var file = new Blob([content], { type: contentType });
        a.href = URL.createObjectURL(file);
        a.download = fileName;
        a.click(); /* Why click? */
    }

    /* Extract data store from indexedDB by name */
    async function getStoreData(transaction, storeName) {
        console.log("Extracting:", storeName);
        return new Promise((resolve, reject) => {
            var request = transaction.objectStore(storeName).getAll();
            request.onsuccess = function(event) {
                resolve(event.target.result); /* Store data is in event.target.result */
            };
            request.onerror = function(event) {
                console.error("Error reading:", storeName, event);
                reject(event);
            };
        });
    }

    /* List of the known relevant data stores */
    var storeNames = ["listGroups", "lists", "tasks", "steps", "linkedEntities"];
    var db = null;
    var transaction = null;
    var storeData = null;
    var todoData = {};
    var todoData_string = "";

    /* IndexedDB name corresponds to unique MS account code (?) */
    var dbName = "".concat("todo_", window.localStorage.getItem("user_id"));
    var request = indexedDB.open(dbName);

    request.onerror = function(event) {
        console.error("Error opening db:", event.target.errorCode);
    };
    request.onsuccess = function(event) {
        let dbPromise1 = new Promise(resolve => {
            db = event.target.result;

            /* Open transaction channel with indexedDB to selected data stores */
            transaction = db.transaction(storeNames, "readonly");
            (async function() {
                /* Data stores are prepended, so top comes last (reverse()) */
                /* Order doesn't actually matter though */
                for (const storeName of storeNames.reverse()) {
                    storeData = await getStoreData(transaction, storeName);
                    console.log("Extracted: ", storeName);
                    todoData = Object.assign({ [storeName]: storeData }, todoData);
                }
                resolve(null);
            })();
        });
        /* Must wait until all data stores have been extracted */
        dbPromise1.then(() => {
            todoData_string = JSON.stringify(todoData, null, 4);
            /* TODO: Add date to download name */
            /* var dateString = new Date(Date.now()).toLocaleDateString */
            download(todoData_string, "".concat(dbName, ".json"), "application/json");
        });
    };
})();
