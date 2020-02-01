javascript: (function() {
    function download(content, fileName, contentType) {
        var a = document.createElement("a");
        var file = new Blob([content], { type: contentType });
        a.href = URL.createObjectURL(file);
        a.download = fileName;
        a.click();
    }

    async function getStoreData(transaction, storeName) {
        console.log("Extracting:", storeName);
        return new Promise((resolve, reject) => {
            var request = transaction.objectStore(storeName).getAll();
            request.onsuccess = function(event) {
                resolve(event.target.result);
            };
            request.onerror = function(event) {
                console.error("Error reading:", storeName, event);
                reject(event);
            };
        });
    }

    var storeNames = ["listGroups", "lists", "tasks", "steps", "linkedEntities"];
    var db = null;
    var transaction = null;
    var storeData = null;
    var todoData = {};
    var todoData_string = "";

    var dbName = "".concat("todo_", window.localStorage.getItem("user_id"));
    var request = indexedDB.open(dbName);

    request.onerror = function(event) {
        console.error("Error opening db:", event.target.errorCode);
    };
    request.onsuccess = function(event) {
        let dbPromise1 = new Promise(resolve => {
            db = event.target.result;

            transaction = db.transaction(storeNames, "readonly");
            (async function() {
                for (const storeName of storeNames.reverse()) {
                    storeData = await getStoreData(transaction, storeName);
                    console.log("Extracted: ", storeName);
                    todoData = Object.assign({ [storeName]: storeData }, todoData);
                }
                resolve(null);
            })();
        });
        dbPromise1.then(() => {
            todoData_string = JSON.stringify(todoData, null, 4);
            download(todoData_string, "".concat(dbName, ".json"), "application/json");
        });
    };
})();
