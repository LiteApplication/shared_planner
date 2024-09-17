
function handleError(toast: any, translator: any, unknown: string = "error.unknown", infos: Object = {}) {
    return ((error: any) => {
        console.log(error);
        error.stack = undefined;
        if (error.response == undefined) {
            toast.add({ severity: 'error', summary: translator('error.title'), detail: translator(unknown) });
            console.error(error);
        } else
            if (error.response?.data) {
                // Check if detail is a string
                if (typeof error.response.data.detail === 'string') {
                    toast.add({ severity: 'error', summary: translator('error.title'), detail: translator(error.response.data.detail, infos) });
                } else {
                    console.error(error.response.data);
                    toast.add({ severity: 'error', summary: translator('error.title'), detail: translator(unknown) });
                }
            } else {
                console.error(error);
                toast.add({ severity: 'error', summary: translator('error.title'), detail: translator(unknown) });
            }
    })

}

export default handleError;